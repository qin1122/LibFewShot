import torch
from torch import digamma, nn
import torch.nn.functional as F
import copy

from core.model.abstract_model import AbstractModel
from core.utils import accuracy
from .meta_model import MetaModel


class Linear_fw(nn.Linear):  # used in MAML to forward input with fast weight
    def __init__(self, in_features, out_features):
        super(Linear_fw, self).__init__(in_features, out_features)
        self.weight.fast = None  # Lazy hack to add fast weight link
        self.bias.fast = None

    def forward(self, x):
        if self.weight.fast is not None and self.bias.fast is not None:
            out = F.linear(x, self.weight.fast,
                           self.bias.fast)  # weight.fast (fast weight) is the temporaily adapted weight
        else:
            out = super(Linear_fw, self).forward(x)
        return out


class Classifier(nn.Module):
    def __init__(self, feat_dim=64, way_num=5) -> None:
        super(Classifier, self).__init__()
        self.layers = nn.Sequential(
            Linear_fw(feat_dim, way_num)
        )

    def forward(self, x):
        return self.layers(x)


class MAML(MetaModel):
    def __init__(self, way_num, shot_num, query_num, feature, device, feat_dim=1600, inner_optim=None,
                 inner_train_iter=10):
        super(MAML, self).__init__(way_num, shot_num, query_num, feature, device)
        self.feat_dim = feat_dim
        self.loss_func = nn.CrossEntropyLoss()
        self.classifier = Classifier(feat_dim, way_num=way_num)
        self.inner_optim = inner_optim
        self.inner_train_iter = inner_train_iter
        self._init_network()

    def set_forward(self, batch, ):
        self.model = nn.Sequential(
            self.model_func,
            self.classifier,
        )
        images, _ = batch
        images = images.to(self.device)
        support_images, query_images, support_targets, query_targets = self.split_by_episode(images, mode=2)
        episode_size, _, c, h, w = support_images.size()

        output_list = []
        loss_list = []
        prec1_list = []
        for i in range(episode_size):
            episode_support_images = support_images[i].contiguous().reshape(-1, c, h, w)
            episode_query_images = query_images[i].contiguous().reshape(-1, c, h, w)
            episode_support_targets = support_targets[i].reshape(-1)
            # episode_query_targets = query_targets[i].reshape(-1)
            self.train_loop(episode_support_images, episode_support_targets)
            output = self.model(episode_query_images)
            loss = self.loss_func(output, query_targets)
            prec1, _ = accuracy(output, query_targets, topk=(1, 3))

            output_list.append(output)
            loss_list.append(loss)
            prec1_list.append(prec1)

        output = torch.cat(output_list, dim=0)
        prec1 = torch.mean(torch.tensor(prec1_list))
        return output, prec1

    def set_forward_loss(self, batch, ):
        self.model = nn.Sequential(
            self.model_func,
            self.classifier,
        )
        images, _ = batch
        images = images.to(self.device)
        support_images, query_images, support_targets, query_targets = self.split_by_episode(images, mode=2)
        episode_size, _, c, h, w = support_images.size()

        output_list = []
        loss_list = []
        prec1_list = []
        for i in range(episode_size):
            episode_support_images = support_images[i].contiguous().reshape(-1, c, h, w)
            episode_query_images = query_images[i].contiguous().reshape(-1, c, h, w)
            episode_support_targets = support_targets[i].reshape(-1)
            # episode_query_targets = query_targets[i].reshape(-1)
            self.train_loop(episode_support_images, episode_support_targets)
            output = self.model(episode_query_images)
            loss = self.loss_func(output, query_targets)
            prec1, _ = accuracy(output, query_targets, topk=(1, 3))

            output_list.append(output)
            loss_list.append(loss)
            prec1_list.append(prec1)

        output = torch.cat(output_list, dim=0)
        loss = torch.mean(torch.stack(loss_list))
        prec1 = torch.mean(torch.tensor(prec1_list))
        return output, prec1, loss

    def train_loop(self, support_set, support_targets):
        lr = self.inner_optim['lr']
        fast_parameters = list(self.parameters())
        for parameter in self.parameters():
            parameter.fast = None

        self.model.train()
        for i in range(self.inner_train_iter):
            output = self.model(support_set)
            loss = self.loss_func(output, support_targets)
            grad = torch.autograd.grad(loss, fast_parameters, create_graph=True)
            fast_parameters = []

            for k, weight in enumerate(self.parameters()):
                if weight.fast is None:
                    weight.fast = weight - lr * grad[k]
                else:
                    weight.fast = weight.fast - self.inner_optim['lr'] * grad[k]
                fast_parameters.append(weight.fast)

    def test_loop(self, *args, **kwargs):
        raise NotImplementedError

    def set_forward_adaptation(self, *args, **kwargs):
        raise NotImplementedError

from torch.utils.data import DataLoader
from torchvision import transforms

from core.data.dataset import GeneralDataset
from .collates import get_collate_fn, get_augment_method
from .samplers import CategoriesSampler
from ..utils import ModelType

MEAN = [120.39586422 / 255.0, 115.59361427 / 255.0, 104.54012653 / 255.0]
STD = [70.68188272 / 255.0, 68.27635443 / 255.0, 72.54505529 / 255.0]


def get_dataloader(config, mode, model_type):
    """

    :param config:
    :param mode:
    :param model_type:
    :return:
    """
    assert model_type != ModelType.ABSTRACT

    trfms_list = []
    if mode == 'train' and config['augment']:
        if config['image_size'] == 224:
            trfms_list.append(transforms.Resize((256, 256)))
            trfms_list.append(transforms.RandomCrop((224, 224)))
        elif config['image_size'] == 84:
            trfms_list.append(transforms.Resize((96, 96)))
            trfms_list.append(transforms.RandomCrop((84, 84)))
        elif config['image_size'] == 80:  # for MTL -> alternative solution: use avgpool(ks=11)
            trfms_list.append(transforms.Resize((92, 92)))  # MTL use another MEAN and STD
            trfms_list.append(transforms.RandomResizedCrop(88))
            trfms_list.append(transforms.CenterCrop((80, 80)))
            trfms_list.append(transforms.RandomHorizontalFlip())
        else:
            raise RuntimeError

        aug_method = get_augment_method(config)
        trfms_list += aug_method
    else:
        if config['image_size'] == 224:
            trfms_list.append(transforms.Resize((256, 256)))
            trfms_list.append(transforms.CenterCrop((224, 224)))
        elif config['image_size'] == 84:
            trfms_list.append(transforms.Resize((96, 96)))
            trfms_list.append(transforms.CenterCrop((84, 84)))
        elif config['image_size'] == 80:  # for MTL -> alternative solution: use avgpool(ks=11)
            trfms_list.append(transforms.Resize((92, 92)))
            trfms_list.append(transforms.CenterCrop((80, 80)))
        else:
            raise RuntimeError


    trfms_list.append(transforms.ToTensor())
    trfms_list.append(transforms.Normalize(mean=MEAN, std=STD))
    trfms = transforms.Compose(trfms_list)

    dataset = GeneralDataset(data_root=config['data_root'], mode=mode,
                             use_memory=config['use_memory'], )

    collate_fn = get_collate_fn(config, trfms, mode, model_type,)

    if mode == 'train' and model_type == ModelType.PRETRAIN:
        dataloader = DataLoader(dataset, batch_size=config['batch_size'], shuffle=True,
                                num_workers=config['n_gpu'] * 4, drop_last=True,
                                pin_memory=True, collate_fn=collate_fn)
    else:
        sampler = CategoriesSampler(label_list=dataset.label_list,
                                    label_num=dataset.label_num,
                                    episode_size=config['episode_size'],
                                    episode_num=config['train_episode']
                                    if mode == 'train' else config['test_episode'],
                                    way_num=config['way_num'],
                                    image_num=config['shot_num'] + config['query_num'])
        dataloader = DataLoader(dataset, batch_sampler=sampler,
                                num_workers=config['n_gpu'] * 4, pin_memory=True, collate_fn=collate_fn)

    return dataloader

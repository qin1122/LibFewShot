# Meta-Learning with Task-Adaptive Loss Function for Few-Shot Learning
## Introduction
| Name:    | [MeTAL](https://arxiv.org/abs/2110.03909) |
|----------|-------------------------------|
| Embed.:  | Conv64F/ResNet12/ |
| Type:    | Meta       |
| Venue:   | ICCV'21                      |
| Codes:   | [**MeTAL**](https://github.com/baiksung/MeTAL) |


Cite this work with:
```bibtex
@inproceedings{baik2021meta,
  title={Meta-learning with task-adaptive loss function for few-shot learning},
  author={Baik, Sungyong and Choi, Janghoon and Kim, Heewon and Cho, Dohee and Min, Jaesik and Lee, Kyoung Mu},
  booktitle={Proceedings of the IEEE/CVF international conference on computer vision},
  pages={9465--9474},
  year={2021}
}
```
---
## Results and Models

**Classification**

|   | Embedding | :book: *mini*ImageNet (5,1) | :computer: *mini*ImageNet (5,1) | :book:*mini*ImageNet (5,5) | :computer: *mini*ImageNet (5,5) | :memo: Comments  |
|---|-----------|--------------------|--------------------|--------------------|--------------------|---|
| 1 | Conv64F | 52.63 ± 0.37% | 53.753 [:arrow_down:](https://drive.google.com/drive/folders/1n6gxu8sWTLMy0hV3LF41FuDx6ajSUuuE?usp=share_link) [:clipboard:](./MeTAL-miniImageNet--ravi-Conv64F-5-1.yaml) | 70.52 ± 0.29% | 71.233 [:arrow_down:](https://drive.google.com/drive/folders/1a9xJdj9qKLxKHQ-CSI8sR_5js47FjFYs?usp=share_link) [:clipboard:](./MeTAL-miniImageNet--ravi-Conv64F-5-5.yaml) | Comments |
| 2 | ResNet12 | 59.64 ± 0.38% | 60.333 [:arrow_down:](https://drive.google.com/drive/folders/1PzVHI_WD6pnqiz_dp56Nav8_pnMFsT4b?usp=sharing) [:clipboard:](./MeTAL-miniImageNet--ravi-resnet12-5-1.yaml) | 76.20 ± 0.19% | 76.800 [:arrow_down:](https://drive.google.com/drive/folders/1zMCmKvL7AkAs1M82_tIYgE5c-0Fs_h_Y?usp=share_link) [:clipboard:](./MeTAL-miniImageNet--ravi-resnet12-5-5.yaml) | Comments |

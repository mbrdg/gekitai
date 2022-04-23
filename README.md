# Gekitai
## IA - L.EIC

- IA first assignment, this project focus on adversarial search in a 2 player,
  turn based, board game.

## Setup

- This porject is meant to be run in a conda environment, however it should
  with `pip` without any problems, just adapt `conda` commands to `pip` commands.
  
  - In case of doubt consult the [documentation](https://docs.conda.io/projects/conda/en/latest/commands.html#conda-vs-pip-vs-virtualenv-commands).

### Dependencies

- The dependencies to run the project are the following:

  - [Numpy](https://numpy.org/)
  - [SciPy](https://scipy.org/)
  - [Pygame](https://pygame.org/)

- In order to create an environment and install the required packages, run:
```bash
$ conda create --name gekitai python
$ conda activate gekitai
(gekitai) $ conda install numpy scipy pip
(gekitai) $ pip install pygame
```

And that's all, now you should be able to run the project from [here](src/gekitai.py).

## Authors

- [João Sousa](mailto:up201904739@edu.fc.up.pt)
- [Miguel Rodrigues](mailto:up201906042@edu.fe.up.pt)
- [Ricardo Ferreira](mailto:up201907835@edu.fe.up.pt)


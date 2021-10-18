# 3Row

Implementation of the 3 In A Row game and make an agent learn to play it.

As a very simple game, the results obtained, even with the collab limitations, are pretty good.

As the gym.ai doesn't allow to play themselves to learn (for now), I couldn't make it ideally play against itself to learn, so for now two implementations of a simple AI rival has been implemented. The first plays randomly (wow, such AI...) and the other one checks if there's an immediate game-winner for the opponent or an immediate winning movement for it, and plays to avoid lose or win the game respectively. The results obtained are on this second one.

It has been tried using a PPOO with rewards as 0 for a draw, 1 for a win, -1 for loss and -10 for an invalid movement. The agent has been not limited to move in any position, although if there is any piece already on that it is considered an invalid move.

The following graphs correspond to the training for 5.000 steps for epoch, 20 epochs and 200 games per evaluation step. The first is the mean score over the 200 games per evaluation:

![Mean Score Training](https://drive.google.com/uc?export=view&id=1NsxuuG3F3tRLu2a939BDqEye2iI3OG34)

The other two are the percentage of victories and the results of the games (victories, losses, etc) respectively:

![Perc Victories](https://drive.google.com/uc?export=view&id=1__NI-hCkonM8CgWAE7X_TrPG6Gkf_H-A)

![Results games](https://drive.google.com/uc?export=view&id=13-epTlGzUz7l199PlaVDb799icQibi37)

Additionally here is a [Link for the Model](https://drive.google.com/file/d/1lFPvwMGN6hU_owFloN8A8tctGiCSwDLj/view?usp=sharing), and you can use it on the ipynb notebook where there is a section where you can try to play against it, I played two games: a loss and draw them, which is pretty impressive.

.
 
 
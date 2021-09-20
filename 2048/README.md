# 2048
Implementation of the 2048 game with Reinforcement Learning.

In general, due to training in collab, I have been very limited to time and memory constraints, so the training has been shorter than what I would like and the learning curve has been stopped when still was increasing in value.

The implementation has been limited to 1000 steps per game, and there are no limited movements, although the ones that cause to not move any piece are considered "invalid" in the rewards.

It has been tried using either DQN or PPOO with different rewards. With DQN no good results are achieved: apart from taking much longer to train, the fact that it learns with a table depending on the state and that there are too many possible states in the game make it almost no progress on learning while training.

With PPOO better results are achieved. The rewards implemented are varied, some of which are:
- the sum of the scores of the pieces on the table, -1 per movement done
- Sum the value of the merged pieces due to the movement plus 1 per movement. Although the score is -100 points, ignoring the rest when doing an invalid movement.
- Same as previous plus the value of the maximum piece on the table
- The value of the merged pieces plus the maximum value of the pieces on the board. Additionally, 3/4 of the maximum value if two pieces with maximum value are together. Ignores all the rest and returns -100 if invalid.

The best results are achieved in the last case when more indications whether how the model should proceed are given. The model with the available time, learns to move right and left and sometimes up, which is not random movements and it starts to appear some strategy used by me when playing the game.

The following graphs correspond to the training for 10.000 steps for epoch, 100 epochs and 300 games per evaluation step. The former is the mean value and the latter is the max value obtained.

![Mean Score Training](https://drive.google.com/uc?export=view&id=1svJYjKhq8N0WyCO4QSKEDmtPQqm-rZrH)

![Max Value Training](https://drive.google.com/uc?export=view&id=1cgBVA_ReIWS9eCYr7WbYtt_64-ZTG9KA)

Additionally there is a link where you can see a video where it plays a game [Link To The Video](https://drive.google.com/file/d/18thnzPIuI_pKz1Rn2o_q0_SoELZUyXvt/view?usp=sharing).
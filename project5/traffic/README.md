##Project 5 - Traffic

1. I start off with nothing but one "Flatten" layer and a dense layer. The activation function is the default linear.

```
Layer (type)                 Output Shape              Param #
=================================================================
flatten (Flatten)            (None, 2700)              0
_________________________________________________________________
dense (Dense)                (None, 43)                116143
=================================================================

...


Epoch 10/10
500/500 [==============================] - 1s 1ms/step - loss: 0.4805 - accuracy: 0.9060
333/333 - 0s - loss: 0.5381 - accuracy: 0.8800
```

It's already pretty good

2. I tried the same thing but with a sigmoid activation function.

```
Epoch 10/10
500/500 [==============================] - 1s 1ms/step - loss: 3.1817 - accuracy: 0.0482
333/333 - 0s - loss: 3.1848 - accuracy: 0.0426
```

At this point I figured that since there's already only one layer, an activation function might add to the constraints. Maybe our neural network didn't have enough freedom to be properly trained.

3. So then I added two more dense layers of the same size, all of them with sigmoid activation functions.

```
Epoch 10/10
500/500 [==============================] - 1s 2ms/step - loss: 3.0800 - accuracy: 0.3432
333/333 - 0s - loss: 3.0794 - accuracy: 0.3529
```

It's an improvement, but it still isn't as good as one layer with no activation function.

4. I did a few more experiments with different activation functions on dense layers but nothing beat the first case. Now, I decided to add Conv2D and MaxPooling2D layers


```_________________________________________________________________
Model: "sequential"
_________________________________________________________________
Layer (type)                 Output Shape              Param #
=================================================================
conv2d (Conv2D)              (None, 30, 30, 32)        896
_________________________________________________________________
max_pooling2d (MaxPooling2D) (None, 15, 15, 32)        0
_________________________________________________________________
dense (Dense)                (None, 15, 15, 10)        330
_________________________________________________________________
dense_1 (Dense)              (None, 15, 15, 43)        473
_________________________________________________________________
flatten (Flatten)            (None, 9675)              0
_________________________________________________________________
dense_2 (Dense)              (None, 43)                416068
=================================================================

...

Epoch 10/10
500/500 [==============================] - 8s 16ms/step - loss: 0.0608 - accuracy: 0.9839
333/333 - 2s - loss: 0.2703 - accuracy: 0.9550

```

Drastic improvement.

5. I added a tanh activation to Conv2D


```Epoch 10/10
500/500 [==============================] - 9s 18ms/step - loss: 0.0447 - accuracy: 0.9877
333/333 - 2s - loss: 0.2429 - accuracy: 0.9580```

There's slightly more improvement

6. I added one more Conv2D layer with relu as its activation function


```Epoch 10/10
500/500 [==============================] - 7s 13ms/step - loss: 0.0230 - accuracy: 0.9930
333/333 - 1s - loss: 0.0982 - accuracy: 0.9769```

7. I added a dropout layer after the conv2d and maxpooling layers

```
Epoch 10/10
500/500 [==============================] - 7s 13ms/step - loss: 0.0357 - accuracy: 0.9891
333/333 - 1s - loss: 0.0837 - accuracy: 0.9810```

8. I added one more Conv2D layer after the dropout layer

```_________________________________________________________________
Epoch 1/10
500/500 [==============================] - 7s 14ms/step - loss: 1.2346 - accuracy: 0.6637
Epoch 2/10
500/500 [==============================] - 7s 14ms/step - loss: 0.2549 - accuracy: 0.9277
Epoch 3/10
500/500 [==============================] - 9s 17ms/step - loss: 0.1504 - accuracy: 0.9558
Epoch 4/10
500/500 [==============================] - 8s 17ms/step - loss: 0.1040 - accuracy: 0.9693
Epoch 5/10
500/500 [==============================] - 8s 16ms/step - loss: 0.0900 - accuracy: 0.9725
Epoch 6/10
500/500 [==============================] - 8s 16ms/step - loss: 0.0631 - accuracy: 0.9810
Epoch 7/10
500/500 [==============================] - 8s 16ms/step - loss: 0.0582 - accuracy: 0.9822
Epoch 8/10
500/500 [==============================] - 8s 16ms/step - loss: 0.0475 - accuracy: 0.9839
Epoch 9/10
500/500 [==============================] - 8s 16ms/step - loss: 0.0415 - accuracy: 0.9868
Epoch 10/10
500/500 [==============================] - 8s 16ms/step - loss: 0.0441 - accuracy: 0.9859
333/333 - 2s - loss: 0.0831 - accuracy: 0.9806```

During training, it got to 0.9 accuracy really fast but still didn't do better than last time. It looks like it got stuck in a corner where it couldn't find any direction for further improvement.

9. I then added another dense layer between the Conv2D layers

```Epoch 10/10
500/500 [==============================] - 11s 21ms/step - loss: 0.0598 - accuracy: 0.9806
333/333 - 2s - loss: 0.0548 - accuracy: 0.9873```

I tried testing a few other things with layers and loss functions but haven't gotten any more improvement than this.
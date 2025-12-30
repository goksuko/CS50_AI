We have created the images inside result_images folder.

1. We used hill climbing.

That's not to say that this is the best we could do. There might be some other configuration of hospitals that is a global minimum. And this might just be a local minimum, that is, the best of all of its neighbors but maybe not the best in the entire possible state space. And you could search through the entire state space by considering all of the possible configurations for hospitals. 

But ultimately, that's going to be very time intensive, especially as our state space gets bigger and there might be more and more possible states. It's going to take quite a long time to look through all of them. And so being able to use these sort of local search algorithms can often be quite good for trying to find the best solution we can do. And especially if we don't care about doing the best possible and we just care about doing pretty good and finding a pretty good placement of those hospitals, then these methods can be particularly powerful. 

2. Then we used Random-restart to Conduct hill climbing multiple times. Each time, start from a random state. Compare the maxima from every trial, and choose the highest amongst those.
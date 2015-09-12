Ray Tracing Method 4-dimensional Visualization
==============================================

This is 4-dimensional visualization project for ray tracing method in room acoustics.
To run the project install reuqired packages and in your terminal use `python main.py`.

### Requirements:
* Python 3.4
* SIP 4.16.9
* PyQt 5.5
* `PyOpenGL==3.1.0`
* `PyOpenGL_accelerate==3.1.0`

### Additional notes:
The project is still lacking some features.
1. Used sound absorption coefficient (later referred as **alpha**) is an average of all planes coefficients (instead of one coefficient for each plane).
2. There is no collision detection implemented and for now the collisions are based only on room boundaries, meaning that it works correctly only for cubic rooms.
3. The air sound absorption and the path that each particle travels are overlooked.
4. Only specular wave reflections are implemented, missing the diffuse reflections.

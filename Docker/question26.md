```
The image is 2 GB. How do you shrink it?

If my Docker image is 2 GB, I would first inspect it using `docker history` to identify the largest layers.

Then I would use a smaller, suitable base image, implement a multi-stage Docker build, and copy only the application artifacts and runtime dependencies into the final stage.

I would also add a `.dockerignore` file, exclude unnecessary files, install only production dependencies, and clean package caches and temporary files.

Finally, I would rebuild the image, compare its size, test the application, and scan it for vulnerabilities.

My goal is to make the image smaller, faster to pull and deploy, and more secure without affecting application functionality.
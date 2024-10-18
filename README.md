Lifter-Database

Web application that uses MoveNet AI model to collect joint and limb metrics from photos inputted. Stores those as database objects (Lifter, Positional Points, Resources). Uses KNN to compare inserted images as vectors to all the database Lifter objects and outputs the most similar lifter. Uses HTTP methods to insert, update, and delete data.

Movenet: https://www.tensorflow.org/hub/tutorials/movenet
Help with MoveNet implementation: https://youtu.be/SSW9LzOJSus?si=FHFmgB-

Pages
1. AllLifters: List of all lifter metrics in the database with Name, weight, and metrics
2. MatchingLifter: Inserts and image to run against the database models and prints the most similar lifter
3. Resources: To be implemented. Stores resources from all professional lifters from the database including programs, youtube channels, etc.
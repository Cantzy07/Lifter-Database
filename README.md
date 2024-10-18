# Lifter-Database

## Web application that uses MoveNet AI model to collect joint and limb metrics from photos inputted. Stores those as database objects (Lifter, Positional Points, Resources). Uses KNN to compare inserted images as vectors to all the database Lifter objects and outputs the most similar lifter. Uses HTTP methods to insert, update, and delete data. Uses a SQLAlchemy database, React frontend and Flask backend framework.

Movenet: https://www.tensorflow.org/hub/tutorials/movenet
Help with MoveNet implementation: https://youtu.be/SSW9LzOJSus?si=FHFmgB-

# Routed Pages
1. AllLifters: List of all lifter metrics in the database with Name, weight, and metrics
2. MatchingLifter: Inserts and image to run against the database models and prints the most similar lifter
3. Resources: To be implemented. Stores resources from all professional lifters from the database including programs, youtube channels, etc.

# How to use
1. Run the main file in the backend directory to start the app context
2. run "npm run dev" in the frontend directory to start the web application on local host development environment
3. Lifters desired to be in the database need to be manually inserted (haven't made a script to enter top 50 ipf lifter data into the database)
4. Insert desired picture into the MatchingLifter tab to get a most similar lifter.
5. Make sure to input non-blurry full body pictures so MoveNet can rig all joints and limbs, preferably at the start of a big 3 compound lift so that compounds can be compared accordingly
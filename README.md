# Scaffold for Battlecode 2018

The game now supports running with docker AND running without docker. See below for the docker instructions.

## Playing with docker

To start, install docker, and make sure it's started.  

### Unix instructions

#### Mac:
Install docker for mac: https://www.docker.com/docker-mac

Clone the repo, or click https://github.com/battlecode/bc18-scaffold/archive/master.zip to download

#### Linux:
Install docker for your system.

Clone the repo, or click and run `sudo sh run.sh` in the directory.  Wait a while to download our code, then finally it will say:

`To play games open http://localhost:6147/run.html in your browser`

Follow its instructions, and start runnin them games! (warning, socket.bc18map may be buggy rn)

### Windows 10 Pro

Windows 10 Professional or Enterprise: install https://www.docker.com/docker-windows

double click run.cmd

wait a while

When you get the message: `To play games open http://localhost:6147/run.html in your browser` you're good to go!

### Writing your own bot

To get started with your bot you can modify one of the examplefuncs-players located in the bc18-scaffold directory. You can modify the run.py for python, the main.c for c, and player.java file for java. Then use the web interface to queue a game as before.

Players are named after the directory where they are located. For example, the player "examplesfuncplayer-python" corresponds to the folder where the python code is located. 

You can create a new player by copying the examplefuncsplayer and then renaming the folder. The website interface can't see your new folder until you refresh the website. Select the website and press F5 or ctrl+r. Your new bot will then appear in the dropdown menu. 

### Check for the latest release

We update the Battlecode game occasionally. Docker should automatically run using the latest version of the Battlecode game. You can manually update to the latest version by entering the following command in the docker quickstart terminal:

docker pull battlecode/battlecode-2018

#### FAQ (for Docker Toolbox):
1. How do I play a game?

 Ignore the variables for the time being unless you want to specifically test something intensive. Select players from the dropdowns on the right as well as a map, and click "Run Game". A pop-up will display showing the logs of each of the 4 bots (2 bots x 2 maps) while the game runs. When the game ends, the pop-up will disappear and the replay will be in the scaffold folder (the same folder where the bots are located).

2. How can I see the replay?

 #### Better
 
 Use the [Tiny Viewer](http://anthonybau.com/bc18-tinyview/)
 
 #### Worse (Official Viewer)
 
 Download the viewer client from http://battlecode.org/#/materials/releases for your operating system. Click on the button with 3 horizontal bars, which will bring up a filesystem that you can select the replay from. Navigate to it, click on the replay, and click "select" in the bottom right of the filesystem window. Then, click the play button in the top right. You can zoom out using the mouse wheel and move your vision using WASD or the arrow keys.

3. I ran a game with a broken bot, and now I can't run another game!

 Open another Docker Quickstart window (start.sh) and type the following command: `docker ps`. This will display the information of the currently running container. Take note of the container ID (the first entry) and type `docker kill {ID}`. You only need to type the first couple characters, e.g. `docker kill e06`. Go back to the original quickstart window and type `bash run.sh` again.

6. Docker is taking up too much memory! / I get out of memory errors when running `run.sh`!

 Docker saves some information between runs called images, containers, and volumes. Unchecked, these can quickly take over many gigs of storage. Occasionally, run the following 4 lines:

 `docker stop $(docker ps -q)`
`docker container rm $(docker container ls -aq)`
`docker volume rm $(docker volume ls -q)$`
`docker volume prune`

 which should free up a lot of space.

 See also https://zaiste.net/posts/removing_docker_containers/

8. I don't see any players/maps in the dropdown and/or my console says that `/player` can't be found!

 This one is pretty tricky to track down. Try looking at your `run.sh` file and changing `/players` to `/player` if necessary. You can also try running the `pwd` command in your scaffold directory and replacing `$PWD` in `run.sh` with that absolute path. Additionally make sure your filepath doesn't contain any spaces, special characters, etc. that may confuse the parser.

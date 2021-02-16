===================
Running the game
===================

Installing
==========

Make sure to uninstall the visual studio version of python if you have visual studio installed. 
You can do this by re-running the installer and unselecting the python development kit then clicking update

***Other Instructions needed***

You can use any text editor for this competition, but we recommend visual studio code.


Running the game
================

Building the launcher
---------------------

When updates are pushed, (run python launcher.pyz u?). Then run build.bat.


Generating the map
------------------

You can generate a new game map by calling

.. code-block:: python

    python launcher.pyz g

within a terminal. You can keep the same game map by just not running the above command


Running the game
-----------------

You can run the bot by calling

.. code-block:: python

    python launcher.pyz g

within the terminal. Print statements within your client will print if you wish to use them for debugging purposes. Alternatively, you can view
the turn logs that are produced within the logs folder


Running the visualize
---------------------

As a third option for debugging, we have built a visualizer! The visualizer visually depicts the logs that are produced, so you can more easily decipher what went wrong. 
The visualizer can be run within

.. code-block:: python
.. code-block:: python

    python launcher.pyz v

    python launcher.pyz v


Improving the bot
-----------------

All improvements should be made within the client. We provide a base client but you are welcome to rename the file or create multiple client files. Make sure to check the
documentation for hints on how to improve!


Scrimmage!
==========

The actual competition occurs on the scrimmage server! You can connect to the 
scrimmage server by running 

.. code-block:: python

    python launcher.pyz scrimmage

After connecting there are 4 commands you can run 

register
----------

registering is required to enter the competition. Once you provide a team name, a vID will be downloaded you your computer. this vID is required to upload your client to the 
server under your team name, so don't delete it! If your teamates wish to upload to the server, you'll have to send them the vID


submit
--------

Once you've registered, you can submit your client. Atleast one client must be submitted by midnight to be elligable to win. The server will automatically look for files in the 
root directory that contain the word 'client'. Otherwise, you can manually select the file. Once you've confirmed the file, it will be uploaded to the server and 
then run 30 times to create an average score. Feel free to submit as many times as you like, but please refrain from excessive uploads.


view stats
------------

Returns stats relating to your submission/s. All stats relate to your most recent submission. Please note that the stats will continue to change until all runs are completed.


leaderboard
--------------

Returns the leaderboard.





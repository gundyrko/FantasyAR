## VE441 Team: FantasyAR



![cover](cover.png)

### Getting Started

First, download _Google Play Service for AR_ from Google Play or Android app store, in order to ensure the AR function works properly.

To set up the server, please refer to [VE441 Lab1](https://eecs441.eecs.umich.edu/ji-asns/lab1-chatter-backend#chatter-back-end).

For the main project, please refer to the [Plastic SCM repo](https://www.plasticscm.com/orgs/gundyrko/repos/FantasyAR/branch/main/tree). You can simply download the code and assets, there's no need to install extra libraries manually. Nevertheless, we still list the third-party SDKs below.

#### Third-party SDK

|    **Libraries**    | **Version** | **Description**                                              | Link                                                         |
| :-----------------: | :---------: | :----------------------------------------------------------- | :----------------------------------------------------------- |
| Unity AR Foundation |   4.1.10    | Present an interface for Unity developers to use AR features | https://unity.com/unity/features/ar                          |
|        GoMap        |    3.7.1    | A dynamic map SDK for making location-based games in Unity   | https://assetstore.unity.com/packages/tools/integration/go-map-3d-map-for-ar-gaming-68889 |
|    Recognissimo     |    1.3.1    | A cross-platform offline speech recognition plugin for Unity | https://assetstore.unity.com/packages/tools/audio/recognissimo-cross-platform-offline-speech-recognition-203101 |



### Model and Engine

#### Storymap

The following pictures shows our story map.

![story_map1](story_map1.png)

![story_map2](story_map2.png)

In summary, a user will first see a 3D map that shows his/her location and the locations of nearby monsters. He/she can view the status and buy/change skills and weapons to prepare for the battle. During the battle, the user can move around to shoot and use voice-controlled skills. In the meantime, the monster will chase and attack the user. Once the monster is defeated, the user gains experience and money.

#### Block Diagram

The following picture is our engine architecture.

![Engine_Architecture](Engine_Architecture.jpg)

We use Unity as our game engine.  Firstly, the front end provides the user location to the unity. With that information, unity can display the map and user avatar with the GO Map. Secondly, the front end provides the voice input, then Recognissimo will transfer it into a string in unity that acts as skill commands. Finally, the back end provides the enemy location to the unity, and with the scene captured by the phone's camera, AR Foundation will generate a game scene with the enemy in the real-time scene.

GO Map and Recognissimo are downloaded from the unity asset store, while ARFoundation is a built-in package of Unity. They are packed perfectly and can communicate with the unity game engine automatically.

1. The first third-party API is GO Map. It can display the map in the real world based on user location, similar to Google Maps but with a game-style look. It will serve as a minimap that indicates to the player where the enemy or new missions are. The input for GO Map is the user location provided by GPS, the output is the minimap as well as the player avatar in the unity engine.

2. The second API is AR Foundation. It can display AR models at specific locations as if the model is live in the scene captured by the camera. The input is the location of the monster in the real world, the output is to instantiate a monster model at that point in the unity engine.

3. The third API is Recognissimo, which is used for voice recognition. With the voice input by the user, it can convert the input into strings in unity. And then, skill commands in the game will be activated accordingly. The input is the user's voice, and the output is a string type to the unity engine.


### APIs and Controller

The APIs used in the backend are shown below:

#### GetEnemyLocation

This function is to ensure that multiple players will see the same enemy in one location so that they can cooperate online.

**Request Parameters**

| Name           | Type    | Description                |
| -------------- | ------- | -------------------------- |
| PlayerLocation | Vector3 | The location of the player |

**Return Parameters**

| Name           | Type           | Description                             |
| -------------- | -------------- | --------------------------------------- |
| EnemyLocations | List<Vector3\> | The location of enemies near the player |
| EnemyTypes     | List<int\>     | The corresponding enemy type index      |



#### GetPlayerLevel

This function is used to get the player level that will be used for the scoreboard.

**Request Parameters**

| Name     | Type | Description             |
| -------- | ---- | ----------------------- |
| PlayerID | int  | Unique ID of the player |

**Return Parameters**

| Name  | Type | Description                     |
| ----- | ---- | ------------------------------- |
| Level | int  | The current level of the player |



#### GetPlayerSkill

This function is used to get the skills that the player has mastered.

**Request Parameters**

| Name     | Type | Description             |
| -------- | ---- | ----------------------- |
| PlayerID | int  | Unique ID of the player |

**Return Parameters**

| Name   | Type       | Description           |
| ------ | ---------- | --------------------- |
| Skills | List<int\> | A List of skill index |



### View UI/UX

The overview of UI/UX. It includes four major parts: Start game and view map, AR battle, Practice mode and Change weapons and skills.

![UI overview](UI_overview.png)

The player will first enter the game and then the player will be able to see the Main Map. When a player is close to one of the monsters. He can enter the battle with that monster by tapping on the monster icon on the map. During the battle, if the monster is successfully defeated, then the player will get experience and money.

The player can also choose to enter the practice mode, which allows the player to manually place a monster on any detected planes, so that the player do not have to go to a specific location to fight with the monster. However, the player will not gain any experience or money in the practice mode. Also, the player can view his level and money, and change his weapons and skills by tapping on the status button.


#### Start game and view map

![start and map](start_and_map.png)

In this flow, the player can start the game, view real-time 3D map and view monster locations on the map.

#### AR battle

![battle](battle.png)

In this flow, the player can shoot the monster, use skills by voice control, gain experience and coins after battle and quit battle.

#### Pratice mode

![practice](practice.png)

This flow is similar to the AR battle. The difference is that player should place a monster on a plane first and player do not gain experience and coins after battle.

#### Change weapons and skills

![store](store.png)

In this flow, the player can view status (level, coins), change weapons and skills.

#### Final Design Justification

![design change](design_change.png)

The change is that we made the crosshair at the center of the battle scene less obvious and made the size of the shoot button larger with a bold border line.

**Mockup Usability Test results**

| Tasks                           | Evaluation Metrics | Evaluation Metrics(% success) |
| ------------------------------- | ------------------ | ----------------------------- |
| Shoot the monster for one time. | ≤ 5 seconds.       | 33                            |

We only list the result of the major fault in the original design. No changes to other UI elements, because more than 80% of the participants did well in other tests. 

For the complete results of usability testing, please see the [google slides](https://docs.google.com/presentation/d/1Lx3SiQz4-HtTHlB96S4Q2PONFLGE1FXCIjDZi7XFGIE/edit?usp=sharing) for details.

### Team Roster

Name: Qihan Ren

Contribution:

- Project manager
- Voice control of skills
- Place a monster on the plane (partial participation, mainly debugging the instantiation of the monster)
- Monster moving AI (partial participation, mainly debugging the monster navigation system)
- Monster attacking (projectile, can be dodged)
- Game over (player death)


Name: Zesheng Yu

Contribution:

- Set up the back-end server and the database for monsters' information
- Implement the API for generating reasonable monsters within the neighbor of user's location
- Implement the API for removing monsters from database
- Implement the API for adding monsters into database
- Organize the back-end server to avoid the potential problem due to concurrent requests.
- Communicate with front-end to place monsters at specific places
- Communicate with front-end to remove monster at the specific place when it is defeated in non-practice mode


Name: Yanjun Chen

Contribution:

- Process map api and 3D Map display
- Place a monster on the plane
- Communicate with back-end to place monster at specific places
- Explore method to combine GPS and AR.



Name: Zhongqian Duan

Contribution:

- Monster model / animation / moving AI
- Skill effect (Fireball, Icelance, Unlimited Blade Works)
- Gun system
- Shop (buy new weapon or skills)
- State (show owned and equipped items / change equipment)
- Local archive (partial participation,  load it when the Shop and State scene starts)
- Health and Damage system (partial participation, link damage to gun and skill)

  

Name: Yangdong Huang

Contribution:

- Monster placement on a plane in the practice mode (creation of AR session and plane detection)
- Player shooting (partial participation, mainly interaction with game loop control)
- Monster health system
- Practice / Battle mode game loop
- Graphical User Interface (buttons and success screen)
- Save and load system

**Note: Only the backend code is pushed to github. Code for other features are on Plastic SCM.**

We came across several challenges during the development. The first challenge is how to write the monster AI in AR mode. The monster should behave differently when the player is close or far away from the monster. Finally, we created an invisible plane for the AR monster to walk on, and managed to make use of the built-in navigation system in Unity. In this process, we also dealt with several weird bugs that did not happen in the Unity Editor but happened in the real AR mode. The second challenge is the poor preciseness of the third-party SDK AR+GPS location. Originally, we planned to use this SDK to instantiate AR monsters at given GPS locations. However, after testing outdoors, we found that the precision of the monster location was poor, deviating from the intended location by greater than 20 meters. Finally, we took an alternative method. We only allow the player to enter the battle when he/she is very close to a monster location, and instantiate the monster locally after he/she enters the battle scene. The third challenge is the interaction between the shop, player status and the save file. We used a Unity UI element named toggle, but were not able to get the current status of the toggle (on or off). Finally, we decided to make interaction with the save file every time we need the toggle status or update the toggle status.

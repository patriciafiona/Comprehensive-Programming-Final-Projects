# Comprehensive Programming Final Projects
 
 <p align="center">
  <img src="https://user-images.githubusercontent.com/32255348/141665254-f34fb5fb-099c-4d23-8ac8-85e0e33b418b.png" width="300" />
</p>

<p align="center"><i><b>Figure 1</b> Preview of Flappy Bird Game</i></p>

<br/>

Result of Flappy Bird Porting Game Project, requirement for pass Comprehensive Programming Class in Nanjing Xiaozhuang University. Developed using C++ and Python.

## Information
<p align="center">
  <img src="https://upload.wikimedia.org/wikipedia/id/d/db/Flappy_Bird_logo.jpg" width="200"/>
</p>

<p align="center"><i><b>Figure 2</b> Flappy Bird Logo</i></p>

```diff
Projects Name         : Flappy Bird

Creator               : Patricia Fiona - 王佳佳

Student ID            : L20253009

Type                  : Final Project (Nanjing Xiaozhuang University)

Platform              : PC

Programming Language  : [C++](https://isocpp.org/) & [Python](https://www.python.org/)

Disclaimer            : This projects is only for study purpose only!
```

## Project Running Preparation
### A. SFML
Here I using Visual Studio 2019 for running the C++ project with SFML. The steps that you must prepare for running this project are:

1. First, you must download the SFML SDK from the [download page](https://www.sfml-dev.org/download.php). You can then unpack the SFML archive wherever you like.
2. Open the C++ game project in Visual Studio
3. Open project **properties** by right click in the project name
<p align="center">
  <img src="https://user-images.githubusercontent.com/32255348/141665964-bb084e3a-85d0-4fea-8c9d-a28451d60f95.png" width="800" />
</p>

<p align="center"><i><b>Figure 3</b> Open Properties by Right Click in the Project Name</i></p>

4. In the project's properties, add:
   - The path to the SFML headers (<sfml-install-path>/include) to C/C++ » General » Additional Include Directories
   - The path to the SFML libraries (<sfml-install-path>/lib) to Linker » General » Additional Library Directories

   These paths are the same in both Debug and Release configuration, so you can set them globally for your project ("All configurations").
   <p align="center">
     <img src="https://user-images.githubusercontent.com/32255348/141666045-8c68bac7-d814-4ec0-ac54-50319861f044.png" width="600" />
   </p>

   <p align="center"><i><b>Figure 4</b> Set the SFML include Location</i></p>

   <p align="center">
     <img src="https://user-images.githubusercontent.com/32255348/141666125-ad58db7a-b7f7-4fff-951f-1dda45cb95ce.png" width="600" />
   </p>

   <p align="center"><i><b>Figure 5</b> Set the SFML lib Location</i></p>

 5. The next step is to link your application to the SFML libraries (.lib files) that your code will need. SFML is made of 5 modules (system, window, graphics, network and audio), and there's one library for each of them.
 
   Libraries must be added in the project's properties, in Linker » Input » Additional Dependencies. Add all the SFML libraries that you need, for example "sfml-graphics.lib", "sfml-window.lib" and "sfml-system.lib".
   
  In this project we will add this libraries:
   - **sfml-graphics-d.lib**
   - **sfml-window-d.lib**
   - **sfml-system-d.lib**
   - **sfml-network-d.lib**
   - **sfml-audio-d.lib**
 
   <p align="center">
     <img src="https://user-images.githubusercontent.com/32255348/141666213-7debc262-9df8-47b2-a70d-ad1c4252f0d7.png" width="400" />
     <img src="https://user-images.githubusercontent.com/32255348/141666245-83734567-1074-4090-8dfc-d40ab10d8766.png" width="400" />
   </p>

   <p align="center"><i><b>Figure 6</b> Set the SFML lib that We want to Use</i></p>
 
 6. Because here I use dynamic version of SFML, we can save the setting by click **Apply** and **Ok**.
 
 ```diff
 -More Details about the setting can be seen in SFML Official Website (https://www.sfml-dev.org/tutorials/2.5/start-vc.php)-
 ``` 
 
  7. Now you can run the game

### B. Python Environment
Here I use **conda environment** that use Anaconda App to create python game environment. If you don't have Anaconda App, you can still prepare the environment by using the steps that you can search by yourself and make sure that you already have **Python** in your computer. The process of preparing the enviroment can be seen in the bottom instructions:
 1. Open Anaconda Promp
 2. To create an environment:
 ```diff
 conda create --name {NAME_OF_YOUR_ENVIRONMENT} python=3.8
 ``` 
   For Example:
 
   <p align="center">
     <img src="https://user-images.githubusercontent.com/32255348/141667453-6bc269ee-3a5d-4fda-ad48-e00dbd07e551.png" width="600" />
   </p>

   <p align="center"><i><b>Figure 7</b> Create Python Environment with Conda</i></p>
 
 3. Activate your Environment by running this code:
 ```diff
 conda activate {NAME_OF_YOUR_ENVIRONMENT}
 ``` 
 
   <p align="center">
     <img src="https://user-images.githubusercontent.com/32255348/141666730-38ae66ae-7690-45a7-8b83-e77cfc1fa419.png" width="600" />
   </p>

   <p align="center"><i><b>Figure 8</b> Activate Conda Environment</i></p>
 
 4. Install PyGame in your environment by running this code:
 ```diff
 pip install pygame 
               OR
 conda install -c cogsci pygame 
 ``` 
 
   <p align="center">
     <img src="https://user-images.githubusercontent.com/32255348/141667466-991244f7-0931-468e-b4d6-5197706ef4c5.png" width="600" />
   </p>

   <p align="center"><i><b>Figure 9</b> Install PyGame Library in Environment</i></p>

 5. You can check your list of libraries by runing this code:
 
  ```diff
 pip list
 ``` 
 
   <p align="center">
     <img src="https://user-images.githubusercontent.com/32255348/141667478-109ecdf1-66ca-49a0-8f71-85c868148c42.png" width="600" />
   </p>

   <p align="center"><i><b>Figure 10</b> Checking List of Libraries in Environment</i></p>
 
 6. Open the Python Project in Visual Studio
 
 7. Choose the **Environment** by choose **Add Environment**
 
 <p align="center">
   <img src="https://user-images.githubusercontent.com/32255348/141667512-89a89a02-d970-4b61-ac74-38e241764033.png" width="800" />
 </p>

 <p align="center"><i><b>Figure 11</b> Add Python Environmet in Visual Studio 2019</i></p>

 8. Select '**Existing Environment**' ->>> From the Environment section, select '**Your Envirnoment**' ->>> And Click Add
 
  <p align="center">
    <img src="https://user-images.githubusercontent.com/32255348/141667525-8a679cb7-436e-441b-9984-4b1153f689e7.png" width="800" />
  </p>

  <p align="center"><i><b>Figure 12</b> Add your Environment to the Project</i></p>
 
 9. Now you can run the game

 
## Results for App 
| Action                            | Result                                  | Action                            | Result                                  |
| -------------                     |------------------                       | -------------                     |------------------                       |
| C++ Preview                       | <img src="https://user-images.githubusercontent.com/32255348/141665727-be1be38b-ffbb-4be4-b0b5-a7f8315f10b3.gif" width="300" />      | Python Preview             | <img src="https://user-images.githubusercontent.com/32255348/141665725-8c4fc7ef-6958-46df-8a12-0e2be4cd1554.gif" width="300" />      |

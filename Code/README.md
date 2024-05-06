## Gesture Controlled Robotic Car

### create conda virtual environment

```
conda create -p vevn python==3.11

conda activate myenv\
```

### Install all neccesary libraries

```
pip install -r requirements.txt

```

### Arduino sketch

install the required libraries

1. AFMotor
2. SoftwareSerial

```
Arduino Ide -> Tools -> Manage Libraries -> search for above libraries
```

Upload the to arduino uno or any

### HC- 05 connection

```
settings -> bluetooth -> add device ->bluetooth -> select hc - 05 -> put pin as '1234'

```

now to know to which port hc - 05 is connected

```
control panel -> devices and Printers -> search hc 05 -> right click -> properties -> hardware -> here port will be mentioned
```

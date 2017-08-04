## glitchart
Glitch art generator

### Example

#### Original
![Original](https://raw.githubusercontent.com/lqdc/glitch/master/examples/hax0red.jpg)

#### Glitched
![Glitched](https://raw.githubusercontent.com/lqdc/glitch/master/examples/hax0red_glitched.png)

#### Original
![Original2](https://raw.githubusercontent.com/lqdc/glitch/master/examples/statue2.jpg)

#### Glitched
![Glitched2](https://raw.githubusercontent.com/lqdc/glitch/master/examples/statue_glitched2.png)

![Glitched3](https://raw.githubusercontent.com/lqdc/glitch/master/examples/statue_glitched3.png)

![Glitched4](https://raw.githubusercontent.com/lqdc/glitch/master/examples/statue_glitched4.png)

### Installation

##### MacOS
```sh
$ git clone https://github.com/lqdc/glitch.git
$ pip3 install ./glitch
$ which glitchart
/usr/local/bin/glitchart
```

##### Ubuntu
```sh
$ git clone https://github.com/lqdc/glitch.git
$ sudo -H pip3 install ./glitch
$ which glitchart
/usr/local/bin/glitchart
```

### Example Usage
```sh
$ glitchart ./examples/hax0red.jpg --n_iter 10 --output_path=~/out_glitched.png
Data length: 20814
Amount: 0.019709835692516275 | Seed: 0.5700552642437293 | n_iter: 10
```

### Usage
```
usage: glitchart [-h] [--amount AMOUNT] [--seed SEED] [--n_iter N_ITER]
                 [--max_width MAX_WIDTH] [--output_path OUTPUT_PATH] [--png]
                 [-q]
                 img_path

Glitch art generator

positional arguments:
  img_path              Path to image to make glitch art from.

optional arguments:
  -h, --help            show this help message and exit
  --amount AMOUNT       Amount to change pixels by (0 - 1). Default random
                        float 0-1.
  --seed SEED           Location of pixel changed within a window. Default
                        random float 0-1.
  --n_iter N_ITER       Number of pixels (windows) to change. Default random
                        int 0-40.
  --max_width MAX_WIDTH
                        Maximum width of image before resizing and keeping
                        aspect ratio. Default 900.
  --output_path OUTPUT_PATH
                        Output image path. By default appends _glitched to
                        filename
  --png                 Convert to PNG. PNG format tends to be more stable.
                        Normally guesses by output name.
  -q, --quiet           Silence stdout.
```


# Advanced Scientific Calculator
An advanced scientific calculator program made in pure python that allows for both 2D and 3D function plotting, along with differential and integral calculation.

<img width="539" height="412" alt="image" src="https://github.com/user-attachments/assets/316927c5-7b02-4996-9a62-f8d4b893fe7c" />

<br></br>
This program was made with the aim of learning to handle and plot mathematical functions in python using libraries such as `sympy`. Therefore, on top of the functionality described above, it has a 'see code' option in every window, which shows the exact code required to reproduce, using python and sympy, the result being shown on the window.
For example, in the window for the 3D graph drawing, it looks like this:
<br></br>
<img width="1111" height="561" alt="image" src="https://github.com/user-attachments/assets/65408081-e507-4854-9be1-f6285f915aef" />


### Bundling the app to make a windows executable
This program was bundled using the `pyinstaller` module ([see its documentation](https://pyinstaller.org/en/stable/#pyinstaller-manual)), which can be installed using:
```
$ pip install pyinstaller
```

After this, I used the following command to bundle everything into a standalone `.exe` file that doesn't need python (or anything else for that matter) to be installed:
```
$ pyinstaller --onefile --noconsole calculator.py
```

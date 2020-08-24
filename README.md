# RotationConvert
Transforma un ciclo de animación con rotaciones en quaterniones a rotaciones euler y viceversa.

## Descripción
Este addon para Blender puede ser útil por ejemplo para homogeneizar varios clips de animación, también se puede usar para llevar una animación a modo euler con el objetivo de pulir detalles y finalmente convertir la animacion a modo quaternion para tener tu asset optimizado por ejemplo para motores de juego, etc.

## Instalación
1. Descarga este repositorio como .zip
2. En Blender, vaya a Editar> Preferencias> Complementos> Instalar ...
3. Seleccione el .zip descargado
4. Habilite el complemento, que aparecerá en la lista.

## Instrucciones
Una vez instalado, en su ventana principal "3D Viewport" seleccione una armadura y cambie a modo POSE, abra otra ventana de tipo "Dope Sheet" en modo "Action Editor", esta ventana contiene un campo de tipo lista deplegable con los nombres de los clips de animaciones, por último en el panel del addon seleccione el clip que quiere convertir y presione el botón que corresponda, esto tardara un poco dependiendo de la cantidad de keyframes.

![Image description](https://raw.githubusercontent.com/RichardCollao/RotationConvert/master/files/Screenshot_01.png)


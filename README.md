# Floatmotion

**Ziel:**  
Ein 3D Game in Python programmieren, welches ausschliesslich über eine 3D-Bewegungssteuerung (mit Leap Motion) gespielt wird.

**Programmbeschrieb:**  
In diesem 3D Game muss eine Kugel durch einen Gang gesteuert werden. Dabei muss zufällig generierten Hindernissen ausgewichen werden. Je länger das Spiel dauert, desto schneller wird die Kugel, was zu einem steigenden Schwierigkeitsgrad führt.
Die Kugel bewegt sich normalerweise schwebend und fliegt in eine bestimmte Richtung im Raum, wobei die Flugbahn in alle Richtungen und mit verschieden Tempi beeinflusst werden kann. Die Kugel wird durch den Spieler mit Hilfe der 3D-Bewegungssteuerung (Leap Motion) gesteuert, was eine dreidimensionale Steuerung der Kugel ermöglicht.  
Modis: Je nach gewählter Schwierigkeitsstufe sind das Starttempo sowie die Beschleunigung der Kugel unterschiedlich. Auch existiert ein Übungsmodus bei dem der Player nicht sterben kann.
Durch eine bestimmte Handbewegung kann man jederzeit in das Hauptmenü gewechselt werden.
Die Hindernisse:
Der Querschnitt des Ganges ist 3 x 3 Einheiten gross. Die Hindernisse können zwischen 0 und 8 Einheiten im Gangquerschnitt belegen.

**Programmierung:**   
Die 3D-Daten, Bewegungskoordinaten, welche der Bewegungssensor der Leap Motion-Steuerung erzeugt, müssen in das Koordinatensystem meines Games übersetzt und mit dem Python-Programm kompatibel gemacht werden. Das Game wird in PyGame und in PyOpenGL programmiert.

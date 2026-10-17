# Simple words: guide for the Glitch'n lessons

The lesson site has two ways to read every step: **Technical** (the current text) and **Simple** (for kids,
about ages 9 to 13, some reading below grade level, some learning English). You are writing the Simple
English line and the Simple Spanish line for each technical line.

## The one rule that matters most
A kid following the Simple line must do **exactly** what the Technical line says: the same part, the same
number of parts, the same place on the board (top, bottom, left, right, middle, next to, below…), the same
colours, the same order, the same thing to watch or listen for. Simpler words, never a different instruction.
- Never add a detail that the technical line doesn't give (no new colours, sizes, positions or part values).
- Never drop a detail that the technical line gives. If a line names a colour or a position, keep it.
- Keep every chip number (40106, 4040, 4021, 4051): it is printed on the chip, so kids can find it.
- Keep leg/pin numbers ("pin 14" → "leg 14").
- Keep values that help pick the right part when they are given (68 pF → "the tiny 68 pF capacitor").
- If a technical line is already simple, keep it the same (copy it exactly).

## Style
- Short sentences (aim for 15 words or fewer). Two short sentences beat one long one.
- Start with a plain action verb: Put, Add, Take out, Plug in, Unplug, Turn, Touch, Listen, Watch.
- Plain everyday words. Friendly, but no extra chat, jokes or exclamation marks.
- Spanish: Latin American Spanish, **tú** form, same short style. Match the Spanish glossary below.

## Glossary (use these words consistently)
| Technical | Simple English | Simple Spanish |
|---|---|---|
| breadboard | board | tablero |
| center gap | the groove in the middle (of the board) | la ranura del centro (del tablero) |
| power rail(s), top/bottom rail | the power rows along the top/bottom edge | las filas de energía del borde de arriba/abajo |
| + rail / positive / power (as a place) | the plus (+) row | la fila de más (+) |
| ground, ground rail, − rail | the minus (−) row | la fila de menos (−) |
| "power and ground jumpers" (of a chip) | its two power wires: one to plus (+) and one to minus (−) | sus dos cables de energía: uno a más (+) y otro a menos (−) |
| jumper, jumper wire | wire | cable |
| long jumper / short jumper | long wire / short wire | cable largo / cable corto |
| trimmer, trimmer knob, trimpot, pot | knob | perilla |
| pushbutton | button | botón |
| photocell, light-dependent resistor | light sensor | sensor de luz |
| LED, LEDs | light, lights | luz, luces |
| audio jack | jack | conector de audio |
| audio cable, cable | speaker cable | cable del parlante |
| battery connector / battery clip | battery clip | conector de la batería |
| 9V battery | 9-volt battery | batería de 9 voltios |
| output (of an oscillator/chip) | output leg (where the signal comes out) the first time in a step; then "output leg" | pata de salida |
| input | input leg | pata de entrada |
| pin N | leg N | pata N |
| frequency | pitch (for sound) / speed (for blinking) | tono / velocidad |
| tempo | speed of the beat | velocidad del ritmo |
| signal | signal | señal |
| oscillator | oscillator (keep: kids learn this word) | oscilador |
| filter | filter (keep) | filtro |
| high-pass filter | filter that lets high sounds through | filtro que deja pasar los sonidos agudos |
| low-pass filter | filter that lets low sounds through | filtro que deja pasar los sonidos graves |
| probe | touch wire | cable de toque |
| voltage starving / starve of power | starving it of power / give it less power | quitarle energía |
| capacitor, resistor, diode, chip | keep the word (the parts list explains it) | capacitor, resistencia, diodo, chip |
| timing capacitor | the capacitor that sets the speed | el capacitor que marca la velocidad |
| large capacitor (electrolytic, can) | big capacitor (keep "can" if the line says can) | capacitor grande |
| counter (4040) | 4040 chip | chip 4040 |
| circuit | circuit | circuito |

## Lines that appear in more than one lesson (use these exactly)
| Technical | Simple English | Simple Spanish |
|---|---|---|
| Connect the power rails on both sides with two jumpers at the right end of the breadboard. | At the right end of the board, add two wires that join the power rows along the top edge to the power rows along the bottom edge. | En el extremo derecho del tablero, agrega dos cables que unan las filas de energía del borde de arriba con las del borde de abajo. |
| Place the 40106 chip across the center gap, then add its power and ground jumpers. | Put the 40106 chip across the groove in the middle of the board. Then add its two power wires: one to plus (+) and one to minus (−). | Pon el chip 40106 sobre la ranura del centro del tablero. Luego agrega sus dos cables de energía: uno a más (+) y otro a menos (−). |
| Insert the audio jack and plug in the cable. | Push in the jack and plug in the speaker cable. | Coloca el conector de audio y enchufa el cable del parlante. |
| Insert the audio jack. | Push in the jack. | Coloca el conector de audio. |
| Clip the battery connector onto the 9V battery. | Snap the battery clip onto the 9-volt battery. | Encaja el conector de la batería en la batería de 9 voltios. |
| Plug the battery wires into the top power rail. | Plug the battery's two wires into the power rows along the top edge. | Enchufa los dos cables de la batería en las filas de energía del borde de arriba. |
| Unplug the battery's red (+) wire. | Unplug the battery's red wire (the + one). | Desenchufa el cable rojo de la batería (el de +). |
| Add a short jumper from the + rail at the right end. | At the right end, add a short wire from the plus (+) row. | En el extremo derecho, agrega un cable corto desde la fila de más (+). |
| Add a second trimmer and two red jumpers at the top. | Add a second knob and two red wires at the top. | Agrega una segunda perilla y dos cables rojos arriba. |
| Unplug the battery. | Unplug the battery. | Desconecta la batería. |
| Plug the battery back in at the right end. | Plug the battery back in at the right end. | Vuelve a conectar la batería en el extremo derecho. |
| Remove the resistor at the bottom. | Take out the resistor at the bottom. | Quita la resistencia de abajo. |
| Plug in the audio cable. | Plug in the speaker cable. | Enchufa el cable del parlante. |
| Unplug the orange wire. | Unplug the orange wire. | Desenchufa el cable naranja. |
| Two slow oscillators | Two slow oscillators | Dos osciladores lentos |
| Voltage starving | Starving it of power | Quitarle energía |

## Lesson titles
Do **not** rewrite lesson titles: they stay the same in both modes. Do write the Simple summary.

## Where it goes
Each lesson has `lessons/<address>/lesson.simple.json`: under "strings", every technical English line from lesson.json
(summary, step titles, sub-step texts, copied exactly) maps to `{"en": "<simple English>", "es": "<simple Spanish>"}`.
When a lesson's wording changes, update its simple lines too: `tools/build_index.py` lists lines with no simple version.

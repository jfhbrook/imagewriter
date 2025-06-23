100 HOME
110 D$ = CHR$(4)
120 PRINT "Test to Screen"
130 PRINT D$; "PR#1"
140 PRINT "Test to Printer"
150 PRINT CHR$(27);"X"
160 PRINT "Underlined"
170 PRINT CHR$(27);"^"
180 PRINT "Underline Ended"
190 PRINT CHR$(27);"!"
200 PRINT "This is in Boldface"
210 PRINT CHR$(27);CHR$(34)
220 PRINT "Boldface Ended"
230 PRINT CHR$(14)
240 PRINT "This is the Doublewide Mode"
250 PRINT CHR$(15)
260 "This Ends Doublewide Mode"
270 PRINT D$; "PR#0"
280 END

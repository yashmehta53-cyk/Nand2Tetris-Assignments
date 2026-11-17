// Capstone Project – Nand to Tetris I
// Student Roll Number: 2501010142
// Personal Number K: 42
// Capstone box program for K = 42.
// Box: starts at screen row 42, 20 rows tall, 48 pixels (3 words) wide.
// A pressed key draws black; no key clears the same area.

(START)
    @KBD
    D=M
    @BLACK
    D;JNE

    // No key pressed: set drawing value to 0.
    @COLOR
    M=0
    @DRAW
    0;JMP

(BLACK)
    // Key pressed: set drawing value to -1 (all 16 pixels black).
    @COLOR
    M=-1

(DRAW)
    // First screen word at SCREEN + 32*42 = 17728.
    @17728
    D=A
    @ADDR
    M=D

    // Draw 20 screen rows.
    @20
    D=A
    @ROWS
    M=D

(ROWLOOP)
    // Write the selected color into three adjacent words = 48 pixels.
    @COLOR
    D=M
    @ADDR
    A=M
    M=D

    @ADDR
    M=M+1
    @COLOR
    D=M
    @ADDR
    A=M
    M=D

    @ADDR
    M=M+1
    @COLOR
    D=M
    @ADDR
    A=M
    M=D

    // Move from the end of these 3 words to the next screen row.
    @ADDR
    M=M+1
    D=M
    @29
    D=D+A
    @ADDR
    M=D

    // Decrease row counter.
    @ROWS
    M=M-1
    D=M
    @ROWLOOP
    D;JGT

    // Continuously check the keyboard again.
    @START
    0;JMP

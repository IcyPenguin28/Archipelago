# Dumping grounds for potential code injections.


# =================
# IN-GAME MESSAGING
# =================
PENDING_FLAG   = 0x01FFED30
STRING_BUFFER  = 0x01FFEE00
ROUTINE_ADDR   = 0x01FFED38
HOOK_ADDR      = 0x0038B4CC

def install_messaging_hook(self):
    routine = bytes([
        # Load pending flag
        0xFF, 0x01, 0x08, 0x3C, # lui t0, 0x01FF
        0x30, 0xED, 0x08, 0x35, # ori t0, t0, 0xED30        # t0 = 0x01FFED30 (PENDING_FLAG)
        0x00, 0x00, 0x09, 0x8D, # lw t1, 0(t0)              # t1 = *PENDING_FLAG
        0x27, 0x00, 0x20, 0x11, # beq t1, zero, exit        # if flag == 0 -> exit
        0x00, 0x00, 0x00, 0x00, # nop                       # delay slot

        # Set up table bounds
        0xFF, 0x01, 0x0A, 0x3C, # lui t2, 0x01FF
        0x90, 0xD5, 0x4A, 0x35, # ori t2, t2, 0xD590        # t2 = table_start (cursor)
        0xFF, 0x01, 0x0B, 0x3C, # lui t3, 0x01FF
        0x30, 0xED, 0x6B, 0x35, # ori t3, t3, 0xED30        # t3 = table_end

        # loop:
        0x2A, 0x60, 0x4B, 0x01, # slt t4, t2, t3            # t4 = (cursor < end)
        0x20, 0x00, 0x80, 0x11, # beq t4, zero, exit        # if cursor >= end -> exit
        0x00, 0x00, 0x00, 0x00, # nop

        0x00, 0x00, 0x4D, 0x8D, # lw t5, 0(t2)              # t5 = candidate pointer

        # if candidate < 0x00100000
        0x10, 0x00, 0x0E, 0x3C, # lui t6, 0x0010            # t6 = 0x00100000
        0x2A, 0x78, 0xAE, 0x01, # slt t7, t5, t6            # t7 = (candidate < lower bound)
        0x18, 0x00, 0xE0, 0x15, # bne t7, zero, next        # if true -> skip
        0x00, 0x00, 0x00, 0x00, # nop

        # if candidate >= 0x02000000
        0x00, 0x02, 0x0E, 0x3C, # lui t6, 0x0200            # t6 = 0x02000000
        0x2A, 0x78, 0xAE, 0x01, # slt t7, t5, t6            # t7 = (candidate < upper bound)
        0x14, 0x00, 0xE0, 0x11, # beq t7, zero, next        # if >= upper bound -> skip
        0x00, 0x00, 0x00, 0x00, # nop

        # load vtable pointer
        0x00, 0x00, 0xAE, 0x8D, # lw t6, 0(t5)              # t6 = *(candidate)

        # compare vtable == 0x009F5D10
        0x9F, 0x00, 0x0F, 0x3C, # lui t7, 0x009F
        0x10, 0x5D, 0xEF, 0x35, # ori t7, t7, 0x5D10        # t7 = 0x009F5D10
        0x0F, 0x00, 0xCF, 0x15, # bne t6, t7, next          # if not match -> skip
        0x00, 0x00, 0x00, 0x00, # nop

        # found valid object
        0x25, 0x20, 0xA0, 0x01, # move a0, t5               # a0 = candidate
        0xFF, 0x01, 0x05, 0x3C, # lui a1, 0x01FF
        0x00, 0xEE, 0xA5, 0x34, # ori a1, a1, 0xEDE0        # a1 = STRING_BUFFER

        # call FUN_0026E9E0
        0x26, 0x00, 0x18, 0x3C, # lui t8, 0x0026
        0xE0, 0xE9, 0x18, 0x37, # ori t8, t8, 0xE9E0        # t8 = function addr
        # save ra
        0xFC, 0xFF, 0xBD, 0x27,  # addiu sp, sp, -4      # grow stack by 4
        0x00, 0x00, 0xBF, 0xAF,  # sw ra, 0(sp)          # save ra
        # make func call
        0x09, 0xF8, 0x00, 0x03, # jalr t8                   # call function
        0x00, 0x00, 0x00, 0x00, # nop
        # restore ra
        0x00, 0x00, 0xBF, 0x8F,  # lw ra, 0(sp)          # restore ra
        0x04, 0x00, 0xBD, 0x27,  # addiu sp, sp, 4       # shrink stack back

        # clear pending flag
        0x00, 0x00, 0x00, 0xAD, # sw zero, 0(t0)            # *PENDING_FLAG = 0

        # unconditional branch to exit
        0x04, 0x00, 0x00, 0x10, # beq zero, zero, exit      # always branch
        0x00, 0x00, 0x00, 0x00, # nop

        # next:
        0x10, 0x00, 0x4A, 0x21, # addi t2, t2, 0x10         # cursor += 0x10
        0xDF, 0xFF, 0x00, 0x10, # beq zero, zero, loop      # jump back (negative offset)
        0x00, 0x00, 0x00, 0x00, # nop

        # exit:
        0x08, 0x00, 0xE0, 0x03, # jr ra                     # return
        0x00, 0x00, 0x00, 0x00, # nop
    ])
    hook = bytes([0x4E, 0xFB, 0x7F, 0x08])
    # self.write_bytes(ROUTINE_ADDR, routine)
    # self.write_bytes(HOOK_ADDR, hook)

def display_ingame_message(self, msg: str):
    if len(msg) > 159:
        msg = msg[:159]
    utf16 = msg.encode('utf-16-le') + b'\x00\x00'
    # self.write_bytes(STRING_BUFFER, utf16)
    # self.write_u32(PENDING_FLAG, 1)
import sys
from bcc import BPF

b1 = BPF(text="int probe1(void *ctx) { return 0; }")
b1.attach_kprobe(event="sys_clone", fn_name="probe1")

b2 = BPF(text="int probe2(void *ctx) { return 0; }")
b2.attach_kprobe(event="syscall", fn_name="probe2")

b1.trace_print()

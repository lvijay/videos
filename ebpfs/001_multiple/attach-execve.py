import sys
from bcc import BPF

fn_name = sys.argv[1]

program = r"""
int """ + fn_name + r"""(void *ctx) {
  bpf_trace_printk("hello world!");
  return 0;
}
"""

b = BPF(text=program)
syscall = b.get_syscall_fnname("execve")
b.attach_kprobe(event=syscall, fn_name=fn_name)

b.trace_print()

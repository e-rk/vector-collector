volatile int state = 0;

int main(void)
{
  for (int i = 0; i < 100000; i++) {
    volatile int temp = i;
    temp *= 2;
    state = temp;
  }
  return 0;
}

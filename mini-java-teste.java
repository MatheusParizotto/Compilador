class LoopTeste {
    public static void main(String[] args) {
        int i = 0;
        while (i < 5) {
            if (i % 2 == 0) {
                System.out.println("Par");
            } else {
                System.out.println("Ímpar");
            }
            i = i + 1;
        }
    }
}
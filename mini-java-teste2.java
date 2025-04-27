public class Teste {
    public static void main(String[] args) {
        double cont, a, b, c;
        cont = 2;
        while (cont > 0) {
            a = lerDouble();
            b = lerDouble();
            if (a > b) {
                c = a - b;
            } else {
                c = b - a;
            }
            System.out.println(c);
            cont = cont - 1;
        }
        System.out.println(c);
    }
}
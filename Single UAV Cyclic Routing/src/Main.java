import java.util.ArrayList;

/**
 * Created by Tony on 13/9/2016.
 */
public class Main {
    public static void main(String args[]) {
        SingleUAV singleUAV = SingleUAV.getSharedInstance();

        // case 1
        System.out.println("Case 1");
        int[] ST   = {0, 0, 0, 0};
        int[][] FT = {{1, 5, 9, 5}, {5, 1, 5, 9}, {9, 5, 1, 5}, {5, 9, 5, 1}};
        int[] RD   = {20, 40, 20, 40};

        // case 2
//        System.out.println("Case 2");
//        int[] ST   = {0, 0, 0, 0};
//        int[][] FT = {{1, 5, 5, 3}, {5, 1, 5, 3}, {5, 5, 1, 3}, {3, 3, 3, 1}};
//        int[] RD   = {21, 21, 21, 10};

        // case 3
//        System.out.println("Case 3");
//        int[] ST   = {0, 0, 0};
//        int[][] FT = {{1, 3, 5}, {3, 1, 3}, {5, 3, 1}};
//        int[] RD   = {20, 20, 10};

        // case 4
//        System.out.println("Case 4");
//        int[] ST   = {0, 0, 0};
//        int[][] FT = {{1, 5, 5}, {5, 1, 5}, {5, 5, 1}};
//        int[] RD   = {20, 20, 10};

//        for (int i = 0; i < FT.length; i++)
//            for (int j = 0; j < 4; j++)
//                System.out.println("FT[" + i + "][" + j + "] = " + FT[i][j]);

        ArrayList<Integer> route = singleUAV.computeCR(ST, FT, RD);

        int i;

        for (i = 0; i < route.size() - 2; i++) {
            System.out.print(route.get(i) + " -> ");
        }

        System.out.println(route.get(i));
    }
}

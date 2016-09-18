import java.util.ArrayList;

/**
 * Created by Tony on 13/9/2016.
 */
public class Main {
    public static void main(String args[]) {
//
        // case 0
//        System.out.println("Case 0");
//        int[] ST   = {0, 0, 0};
//        int[][] FT = {{0, 5, 5}, {5, 0, 5}, {5, 5, 0}};
//        int[] RD   = {10, 10, 10};

        // case 1
//        System.out.println("Case 1");
//        int[] ST   = {0, 0, 0, 0};
//        int[][] FT = {{0, 5, 9, 5}, {5, 0, 5, 9}, {9, 5, 0, 5}, {5, 9, 5, 0}};
//        int[] RD   = {20, 38, 20, 38};

        // case 2
//        System.out.println("Case 2");
//        int[] ST   = {0, 0, 0, 0};
//        int[][] FT = {{0, 5, 5, 3}, {5, 0, 5, 3}, {5, 5, 0, 3}, {3, 3, 3, 0}};
//        int[] RD   = {21, 21, 21, 10};

        // case 3
//        System.out.println("Case 3");
//        int[] ST   = {0, 0, 0};
//        int[][] FT = {{0, 3, 5}, {3, 0, 3}, {5, 3, 0}};
//        int[] RD   = {20, 20, 10};

        // case 4
//        System.out.println("Case 4");
//        int[] ST   = {0, 0, 0};
//        int[][] FT = {{0, 5, 5}, {5, 0, 5}, {5, 5, 0}};
//        int[] RD   = {20, 20, 10};

        // case 5
//        System.out.println("Case 5");
//        int[] ST   = {0, 0, 0, 0};
//        int[][] FT = {{0, 141,282,423}, {141,0,141,282}, {282,141,0,141}, {423,282,141,0}};
//        int[] RD   = {1412, 1412, 1412, 1412};

        // case 6
//        System.out.println("Case 6");
//        int[] ST   = {0, 0, 0, 0};
//        int[][] FT = {{0, 100,282,424}, {100,0,223,360}, {282,223,0,141}, {424,360,141,0}};
//        int[] RD   = {1490, 1490, 1490, 1490};

        // case 7
        System.out.println("Case 7");
        int[] ST   = {0, 0, 0, 0};
        int[][] FT = {{0, 5, 7, 11}, {5, 0, 3, 6}, {7, 3, 0, 6}, {11, 6, 6, 0}};
        int[] RD   = {25, 26, 27, 27};

        // case 8
//        System.out.println("Case 8");
//        int[] ST   = {0, 0, 0, 0, 0};
//        int[][] FT = {{0, 141,282,423,564}, {141,0,141,282,423}, {283,141,0,141,282}, {424,283,141,0,141}, {564,424,283,141,0}};
//        int[] RD   = {2260, 2260, 2260, 2260, 2260};

        // case 9
//        System.out.println("Case 9");
//        int[] ST   = {0, 0, 0, 0, 0};
//        int[][] FT = {{0, 122,211,172,143}, {122,0,300,211,98}, {211,300,0,122,240}, {172,211,122,0,130}, {143,98,240,130,0}};
//        int[] RD   = {122, 98, 122, 122, 98};

//        // case 10
//        System.out.println("Case 10");
//        int[] ST   = {0, 0, 0, 0};
//        int[][] FT = {{0, 100,360,424}, {100,0,316,360}, {360,316,0,100}, {424,360,100,0}};
//        int[] RD   = {1568, 1568, 1568, 1568};

//        for (int i = 0; i < FT.length; i++)
//            for (int j = 0; j < 4; j++)
//                System.out.println("FT[" + i + "][" + j + "] = " + FT[i][j]);

        SingleUAV singleUAV = new SingleUAV(ST, RD, FT);
        ArrayList<Integer> route = singleUAV.computeCR();

        int i;

        if (route != null) {
            for (i = 0; i < route.size() - 2; i++) {
                System.out.print(route.get(i) + " -> ");
            }

            System.out.println(route.get(i));

            singleUAV.checkCR(route);
        }
        else
            System.out.println("No solution found!");
    }
}

import java.util.ArrayList;
import java.util.Collections;

/**
 * Created by Tony on 11/9/2016.
 */

// Singleton class.
public class SingleUAV {
    private static SingleUAV sharedInstance = null;

    private SingleUAV() {}

    public static SingleUAV getSharedInstance() {
        if (sharedInstance == null) {
            sharedInstance = new SingleUAV();
        }

        return sharedInstance;
    }

    int totalTargets;

    public ArrayList computeCR(int[] ST, int[][] FT, int[] RD) {

        // Initialisation.
        int t = 1;
        totalTargets = ST.length;
        int slotNum = totalTargets;
        int L[] = new int[totalTargets];
        int U[] = new int[totalTargets];
        boolean isSAT = false;

        // Keep track of the target visited at the time slot; the index is the time slot.
        ArrayList<Integer> T = new ArrayList<Integer>();
        T.add(getNextTarget(RD, -1, -1));
        T.add(getNextTarget(RD, -1, T.get(0)));

        System.out.println("Time slot 0: " + T.get(0));

        // Keep track of the time visited at the time slot; the index is the time slot.
        ArrayList<Integer> S = new ArrayList<Integer>();
        S.add(0);
        S.add(FT[T.get(0)][T.get(1)]);

        for (int i = 0; i < totalTargets; i++) {
            L[i] = 0;
            U[i] = 999;

            // Pre-processing of the input.
            for (int j = 0; j < totalTargets; j++) {
                FT[i][j] += 0.5*ST[i] + 0.5*ST[j];

                if (FT[i][j] > 0.5 * RD[i]) return null;
            }
        }

        while (t <= slotNum) {
            int u = T.get(t);  // target visited at the current time slot
            L[u]  = S.get(t);  // update time of last visit for this time slot

            System.out.println("Time slot " + t + ": " + u);

            if (t == slotNum) {
                if (u == T.get(0) && isAllVisited(T)) return T;

                slotNum++;
            }

            // Compute time left to deadline for each target.
            for (int i = 0; i < totalTargets; i++) {
                if (i != T.get(t-1) && i != u)
                    U[i] = RD[i] - (S.get(t) - L[i]);
            }

            int v = getNextTarget(U, u, T.get(t-1));
            int tmp = S.get(t) + FT[u][v];

            for (int i = 0; i < totalTargets; i++) {
                U[i] = 999;  // reset

                // Check if the RD constraints are met.
                if (tmp - L[i] >= RD[i] && i != v) {
                    // does not satisfy

                    T.add(i);
                    S.add(S.get(t) + FT[u][i]);
                    isSAT = false;
                    t++;
                    break;
                }
                else if (tmp - L[i] > RD[i] && i == v) {
                    // does not satisfy

                    T.set(t, v);
                    S.set(t, S.get(t-1) + FT[T.get(t-1)][i]);
                    isSAT = false;
                    slotNum--;
                    break;
                }
                else {
                    // satisfies the constraint

                    isSAT = true;
                }
            }

            if (isSAT) {
                t++;
                T.add(v);
                S.add(tmp);
            }
        }

        return T;
    }

    public boolean isAllVisited(ArrayList<Integer> array) {
        boolean O[] = new boolean[totalTargets];   // keep track of whether target is visited

        for (int i = 0; i < O.length; i++)
            O[i] = false;

        for (int i : array)
            O[i] = true;

        for (boolean i : O)
            if (!i) return false;

        return true;
    }

    public int getNextTarget(int[] array, int curTarget, int prevTarget) {
        int minValue = array[0];
        int nextTarget = 0;

        for (int i = 0; i < array.length; i++) {
            if (array[i] <= minValue && i != curTarget && i != prevTarget) {
                minValue   = array[i];
                nextTarget = i;
            }
        }

        return nextTarget;
    }
}

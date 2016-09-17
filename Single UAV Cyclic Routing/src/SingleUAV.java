import java.lang.reflect.Array;
import java.util.ArrayList;
import java.util.Collections;

/**
 * Created by Tony on 11/9/2016.
 */

// Singleton class.
public class SingleUAV {
    private int[] ST, RD;
    private int[][] FT;

    public SingleUAV(int[] ST, int[] RD, int[][] FT) {
        this.ST = ST;
        this.RD = RD;
        this.FT = FT;
    }

    // Initialisation.
    private int t;
    private int totalTargets;
    private int slotNum;
    private int F[];  // keep track of the time slot at which the target is first visited
    private int L[];  // keep track of the time that the target is last visited
    private int U[];
    private int freq[];

    private boolean isSAT = false;

    private ArrayList<Integer> T, S;

    public ArrayList computeCR() {

        // Initialisation.
        t = 1;
        totalTargets = ST.length;
        slotNum = totalTargets;
        F = new int[totalTargets];  // keep track of the time slot at which the target is first visited
        L = new int[totalTargets];  // keep track of the time that the target is last visited
        U = new int[totalTargets];
        freq = new int[totalTargets];

        for (int i = 0; i < totalTargets; i++) {
            F[i] = -1;
            L[i] = freq[i] = 0;
            U[i] = 9999;

            // Pre-processing of the input.
            for (int j = 0; j < totalTargets; j++) {
                FT[i][j] += 0.5*ST[i] + 0.5*ST[j];

                if (FT[i][j] > 0.5 * RD[i]) return null;
            }
        }

        // Keep track of the target visited at the time slot; the index is the time slot.
        T = new ArrayList<>();

        // First target to be visited.
        T.add(getNextTarget(RD, -1, -1));
        F[T.get(0)] = 0;
        freq[T.get(0)]++;

        System.out.println("Time slot 0: " + T.get(0));

        // Second target to be visited.
        T.add(getNextTarget(RD, T.get(0), T.get(0)));

        // Keep track of the time which a target was visited at the time slot;
        // the index is the time slot.
        S = new ArrayList<>();
        S.add(0);
        S.add(FT[T.get(0)][T.get(1)]);

        while (t <= slotNum) {
            int u = T.get(t);  // target visited at the current time slot
            L[u]  = S.get(t);  // update time of last visit for this time slot
            freq[u]++;

            if (F[u] == -1) F[u] = t;

            System.out.println("Time slot " + t + ": " + u);

            if (t == slotNum) {
                if (u == T.get(0) && isAllVisited()) return T;

                slotNum++;
            }

            // Compute time left to deadline for each target.
            for (int i = 0; i < totalTargets; i++) {
                if (i != u)
                    U[i] = RD[i] - (S.get(t) - L[i]);
            }

            int v = getNextTarget(U, u, T.get(t-1));

            if (v == -1) return null;  // cannot find any other route to take

            int tmp = S.get(t) + FT[u][v];

            for (int i = 0; i < totalTargets; i++) {
                U[i] = 9999;  // reset

                
            }

            if (S.get(t) + FT[u][v] - L[v] > RD[v]) {
                // does not satisfy again

                if (F[u] == t) F[u] = -1;  // reset

                T.set(t, v);
                S.set(t, S.get(t-1) + FT[T.get(t-1)][v]);
                slotNum--;

                // Update the last visited time of the target that is being replaced.
                int lastVisit = T.lastIndexOf(u);
                L[u] = (lastVisit != -1) ? S.get(lastVisit) : 0;

                // Update frequency.
                freq[u]--;
            }
            else {
                t++;
                T.add(v);
                S.add(tmp);
            }
        }

        return T;
    }

    private int getNextTarget(int[] array, int curTarget, int prevTarget) {
        ArrayList<Integer> shortestRD = new ArrayList<>();  // targets with shortestRD
        ArrayList<Integer> unvisited  = new ArrayList<>();  // unvisited targets
        ArrayList<Integer> leastFreq = new ArrayList<>();
        int minRD = 9999;
        int minFT = 9999;
        int minFreq = 9999;
        int nextTarget = -1;

//        // Obtain min frequency.
//        for (int i = 0; i < totalTargets; i++)
//            if (freq[i] <= minFreq) minFreq = freq[i];
//
////        System.out.println("Min Freq: " + minFreq);
//
//        // Extract targets with min frequency.
//        for (int i = 0; i < totalTargets; i++) {
////            System.out.println("i: " + i + " Frequency: " + freq[i]);
//
//            if (freq[i] == minFreq) leastFreq.add(i);
//        }
//
////        for (int i : leastFreq) System.out.println("Least Freq: " + i);
//
//        if (leastFreq.size() > 1) {
//            // Obtain min relative deadline.
//            for (int i : leastFreq)
//                if (array[i] <= minRD) minRD = array[i];
//
////            System.out.println("Min RD: " + minRD);
//
//            // Extract targets with min frequency and relative deadline.
//            for (int i : leastFreq)
//                if (array[i] == minRD) shortestRD.add(i);
//
////            for (int i : shortestRD) System.out.println("Shortest RD: " + i);
//
//            if (curTarget == -1) return shortestRD.get(shortestRD.size()-1);
//
//            if (shortestRD.size() > 1) {
//
//                // Extract a target with shortest flight time.
//                for (int i = 0; i < shortestRD.size(); i++)
//                    if (FT[curTarget][shortestRD.get(i)] <= minFT) {
//                        minFT = FT[curTarget][shortestRD.get(i)];
//                        nextTarget = shortestRD.get(i);
//                    }
//            }
//            else
//                nextTarget = shortestRD.get(0);
//        }
//        else
//            nextTarget = leastFreq.get(0);

        for (int i = 0; i < array.length; i++) {
            if (i != curTarget && i != prevTarget && array[i] <= minRD) {
                minRD   = array[i];

                if (curTarget == -1) nextTarget = i;
            }
        }

        if (curTarget != -1) {

            for (int i = 0; i < array.length; i++) {
//                System.out.println("i: " + i + " minRD: " + array[i]);
                if (minRD == array[i]) shortestRD.add(i);
            }

//            for (int j : shortestRD) System.out.println("shortestRD: " + j);

            for (int i : shortestRD) {
                if (F[i] == -1) unvisited.add(i);
            }

//            for (int j : unvisited) System.out.println("unvisited: " + j);

            ArrayList<Integer> tmpAr;

            tmpAr = (!unvisited.isEmpty()) ? unvisited : shortestRD;

//            for (int j : tmpAr) System.out.println("tmpAr: " + j);

            for (int i : tmpAr) {
                if (FT[curTarget][i] <= minFT) {
                    minFT = FT[curTarget][i];
                    nextTarget = i;
                }
            }
        }

        return nextTarget;
    }

    private boolean isAllVisited() {
        for (int i : F)
            if (i == -1) return false;

        return true;
    }

    public void checkCR(ArrayList<Integer> route) {
        int cyclicTime = 0;

        System.out.println("\nValidating Cyclic Route...");

        for (int i = 0; i < route.size() - 1; i++) {
            cyclicTime += FT[route.get(i)][route.get(i+1)];
        }

        System.out.println("\nCyclic Time: " + cyclicTime);

        int[] firstVisit = new int[totalTargets];
        int[] lastVisit  = new int[totalTargets];

        for (int i = 0; i < totalTargets; i++) {
            firstVisit[i] = lastVisit[i] = -1;
        }

        int fwd, bwd;
        fwd = bwd = 0;
        int j = route.size() - 1;

        firstVisit[route.get(0)] = 0;
        lastVisit[route.get(j--)]  = cyclicTime;

        for (int i = 1; i < route.size(); i++) {
            fwd += FT[route.get(i)][route.get(i-1)];

            if (firstVisit[route.get(i)] == -1) firstVisit[route.get(i)] = fwd;

            bwd += FT[route.get(j+1)][route.get(j)];

            if (lastVisit[route.get(j)] == -1) lastVisit[route.get(j)] = cyclicTime - bwd;

            j--;
        }

//        for (int i = 0; i < totalTargets; i++) {
//            System.out.println("i: " + i + " First Visit: " + firstVisit[i] + " Last Visit: " + lastVisit[i]);
//        }

        for (int i = 0; i < totalTargets; i++) {
            if (cyclicTime - lastVisit[i] + firstVisit[i] > RD[i]) {
                System.out.println("Route is wrong!");

                System.out.println("Error @ time slot " + route.lastIndexOf(i) +
                        " where target = " + i +
                        ", RD = " + RD[i]
                );

                return;
            }
        }

        System.out.println("Route is correct!");
    }
}

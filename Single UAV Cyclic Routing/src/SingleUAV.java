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

    private ArrayList<Integer> CR, S, errors;

    int cycle = 1;

    public ArrayList computeCR() {

        // Initialisation.
        t = 1;
        totalTargets = ST.length;
        slotNum = totalTargets;
        F = new int[totalTargets];  // keep track of the time at which each target is first visited
        L = new int[totalTargets];  // keep track of the time at which each target is last visited
        U = new int[totalTargets];  // keep track of the urgency of each target to meet its RD
//        freq = new int[totalTargets];

        for (int i = 0; i < totalTargets; i++) {
            F[i] = -1;
            L[i] = 0;
//            freq[i] = 0;
            U[i] = 9999;

            // Pre-processing of the input.
            for (int j = 0; j < totalTargets; j++) {
                FT[i][j] += 0.5*ST[i] + 0.5*ST[j];

                if (FT[i][j] > 0.5 * RD[i]) return null;
            }
        }

        // Keep track of the target visited at the time slot; the index is the time slot.
        CR = new ArrayList<>();

        // First target to be visited.
        CR.add(getNextTarget(RD, -1, -1));
        F[CR.get(0)] = 0;
//        freq[T.get(0)]++;

        System.out.println("Cycle: ~ -> Time slot 0: " + CR.get(0));

        // Second target to be visited.
        CR.add(getNextTarget(RD, CR.get(0), CR.get(0)));

        // Keep track of the time which a target was visited at the time slot;
        // the index is the time slot.
        S = new ArrayList<>();
        S.add(0);
        S.add(FT[CR.get(0)][CR.get(1)]);

        errors = new ArrayList<>();

        while (t <= slotNum) {
            int u = CR.get(t);  // target visited at the current time slot
            L[u]  = S.get(t);  // update time of last visit for this time slot
//            freq[u]++;

            if (F[u] == -1) F[u] = L[u];

            System.out.println("Cycle: " + cycle + " -> Time slot " + t + ": " + u);

            // A cycle has been formed with the first target (may not have visited all targets.)
            if (u == CR.get(0)) {
                ArrayList<Integer> tempList = new ArrayList<>();

                for (int i = 0; i < totalTargets; i++) {
                    if (F[i] != -1 && S.get(t) - L[i] + F[i] > RD[i]) {
                        /* Here, we're kind of like reversing time and undoing the "past". */

                        // Obtain the time slot at which u is last visited
                        // apart from the current time slot, and replace it.
                        t = CR.subList(0, CR.size()-1).lastIndexOf(u);

                        // Duplicate the sublist to be removed.
                        for (int j = t+1; j < CR.size(); j++)
                            tempList.add(CR.get(j));

                        // Update the cyclic route.
                        CR.subList(t+1, CR.size()).clear();
                        CR.set(t, i);  // replace target in the cyclic route

                        // Update first and last visits of each target that is removed.
                        for (int k : tempList) {
                            F[k] = (CR.indexOf(k) == -1) ? -1 : S.get(CR.indexOf(k));
                            L[k] = (CR.lastIndexOf(k) == -1) ? 0 : S.get(CR.lastIndexOf(k));

//                            System.out.println("i: " + k + " First: " + F[k] + " Last: " + L[k]);
                        }

                        // Update the list of time at which a target is visited.
                        S.subList(t+1, S.size()).clear();

                        u = i;  // update currently visited target

                        if (t == 0) {
                            S.set(t, 0);

                            // Obtain second target to be visited
                            CR.add(getNextTarget(RD, CR.get(0), CR.get(0)));
                            S.add(FT[CR.get(0)][CR.get(1)]);

                            t = 1;
                            u = CR.get(t);
                            L[u] = S.get(t);
                            F[u] = L[u];
                        }
                        else
                            S.set(t, S.get(t-1) + FT[CR.get(t-1)][i]);

                        // Update slotNum; it must be at least the total number of targets.
                        slotNum = (t < totalTargets) ? totalTargets : t;

                        System.out.println("Cycle: " + cycle + " -> Time slot " + t + ": " + u);
                        break;
                    }
                }
            }

            if (t == slotNum) {
                if (u == CR.get(0) && isAllVisited()) {
                    System.out.println(cycle + " cycles.");

                    return CR;
                }

                slotNum++;
            }

            // Compute time left to deadline for each target.
            for (int i = 0; i < totalTargets; i++) {
                if (i != u)
                    U[i] = RD[i] - (S.get(t) - L[i]);
            }

            int v = getNextTarget(U, u, CR.get(t-1));

//            System.out.println("v: " + v);

//            if (v == -1) return null;  // cannot find any other route to take

            for (int i = 0; i < totalTargets; i++) {
                U[i] = 9999;  // reset
            }

            int tmp = S.get(t) + FT[u][v];

            if (tmp - L[v] > RD[v]) {
                // does not satisfy

                if (CR.indexOf(u) == t) F[u] = -1;  // reset

                CR.set(t, v);
                S.set(t, S.get(t-1) + FT[CR.get(t-1)][v]);
                slotNum--;

                // Update the last visited time of the target that is being replaced.
                int lastVisit = CR.lastIndexOf(u);
                L[u] = (lastVisit != -1) ? S.get(lastVisit) : 0;

//                // Update frequency.
//                freq[u]--;
            }
            else {
                t++;
                CR.add(v);
                S.add(tmp);
            }

            u = CR.get(t);  // target visited at the current time slot
            L[u]  = S.get(t);  // update time of last visit for this time slot
//            freq[u]++;

            if (F[u] == -1) F[u] = L[u];

            cycle++;
        }

        return null;
    }

    private int getNextTarget(int[] array, int curTarget, int prevTarget) {
        ArrayList<Integer> shortestRD = new ArrayList<>();  // targets with shortestRD
        ArrayList<Integer> unvisited  = new ArrayList<>();  // unvisited targets
        int minRD = 9999;
        int minFT = 9999;
        int nextTarget = -1;

        // Obtain the min relative deadline whereby
        // the target is not currently or previously visited.
        for (int i = 0; i < array.length; i++) {
            if (i != curTarget && i != prevTarget && array[i] <= minRD) {
                minRD = array[i];

                if (curTarget == -1) nextTarget = i;
            }
        }

        if (curTarget != -1) {
            // Extract targets with the min relative deadline.
            for (int i = 0; i < array.length; i++) {
//                System.out.println("i: " + i + " minRD: " + array[i]);
                if (minRD == array[i]) shortestRD.add(i);
            }

//            for (int j : shortestRD) System.out.println("shortestRD: " + j);

            // Extract targets that are unvisited among those with min RD.
            for (int i : shortestRD) {
                if (F[i] == -1) unvisited.add(i);
            }

//            for (int j : unvisited) System.out.println("unvisited: " + j);

            // Check if there is any unvisited target.
            ArrayList<Integer> tmpAr = (!unvisited.isEmpty()) ? unvisited : shortestRD;

//            for (int j : tmpAr) System.out.println("tmpAr: " + j);

            // Obtain target with the min flight time.
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
        int time[] = new int[route.size()];
        time[0] = 0;

        System.out.println("\nValidating Cyclic Route...");

        if (!isAllVisited()) {
            System.out.println("Route is wrong!");
            return;
        }

        // Compute cyclic time.
        for (int i = 0; i < route.size() - 1; i++) {
            cyclicTime += FT[route.get(i)][route.get(i+1)];
            time[i+1] = cyclicTime;
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
        lastVisit[route.get(j--)] = cyclicTime;

        for (int i = 1; i < route.size(); i++) {
            fwd += FT[route.get(i)][route.get(i-1)];

            if (firstVisit[route.get(i)] == -1) firstVisit[route.get(i)] = fwd;

            bwd += FT[route.get(j+1)][route.get(j)];

            if (lastVisit[route.get(j)] == -1) lastVisit[route.get(j)] = cyclicTime - bwd;

            j--;
        }

        boolean isFound = false;

        for (int i = 0; i < route.size(); i++) {
            int u = route.get(i);

            // Check if the target is visited again within the cycle.
            for (int k = i+1; k < route.size(); k++) {
                if (u == route.get(k)) {
                    if (time[k] - time[i] > RD[u]) {
                        printErrorMessage(i, u);
                        return;
                    }

                    isFound = true;
                    break;
                }
            }

            // The last visited target within the cycle.
            if (!isFound && (cyclicTime - lastVisit[u] + firstVisit[u] > RD[u])) {
                printErrorMessage(i, u);
                return;
            }

            isFound = false; // reset
        }

        System.out.println("Route is valid!");
    }

    private void printErrorMessage(int i, int u) {
        System.out.println("Route is invalid!");
        System.out.println("Error @ time slot " + i +
                " where target = " + u +
                ", RD = " + RD[u]
        );
    }
}

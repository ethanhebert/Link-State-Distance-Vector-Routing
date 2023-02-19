/* Ethan Hebert
 * CSC-325-001
 * 11-5-22
 * Assignment 5 - Graphs
 * Reads an unweighted, undirected graph and a weighted, directed graph from files, creates adjacency matrices for both,
 * finds the BFS and DFS for the first graph and the Dijkstra's Algorithm for the second graph, and outputs this info to a text file.
 */

//import libraries
import java.io.*;
import java.util.*;

public class Main {
    //CLASS VARIABLES
    //file names
    private static final String INPUT_FILE = "input.txt";
    private static final String INPUT_WEIGHTS_FILE = "input_weights.txt";
    private static final String OUTPUT_FILE = "output.txt";
    //starting vertex for each algorithm
    private static final char STARTING_VERTEX_BFS = 'a';
    private static final char STARTING_VERTEX_DFS = 'a';
    private static final char STARTING_VERTEX_DIJKSTRA = 'a';
    //holds each line of the file in an index of a String ArrayList
    private static List<String> linesInput = new ArrayList<String>();
    private static List<String> linesInputWeights = new ArrayList<String>();

    public static void main(String[] args) {
        //NORMAL INPUT
        //read the input
        try {
            Scanner scanner = new Scanner(new File(INPUT_FILE));
            while (scanner.hasNextLine())
                linesInput.add(scanner.nextLine());
            scanner.close();
        } catch (FileNotFoundException e) {
            System.out.println("An error occurred.");
            e.printStackTrace();
        }

        //create the adjacency matrix
        int[][] matrixInput = createAdjacencyMatrix(linesInput, false);


        //WEIGHTED INPUT
        //read the weighted input
        try {
            Scanner scanner = new Scanner(new File(INPUT_WEIGHTS_FILE));
            while (scanner.hasNextLine())
                linesInputWeights.add(scanner.nextLine());
            scanner.close();
        } catch (FileNotFoundException e) {
            System.out.println("An error occurred.");
            e.printStackTrace();
        }

        //create the adjacency matrix
        int[][] matrixInputWeights = createAdjacencyMatrix(linesInputWeights, true);


        //SAVE OUTPUTS TO FILE
        try {
            FileWriter writer = new FileWriter(OUTPUT_FILE);
            writer.write("Adjacency Matrix (undirected):\n");
            writer.write(printAdjacencyMatrix(matrixInput));
            writer.write("BFS: " + BFS(matrixInput, STARTING_VERTEX_BFS) + "\n");
            writer.write("DFS: " + DFS(matrixInput, STARTING_VERTEX_DFS) + "\n\n");
            writer.write("Adjacency Matrix (directed w/weights):\n");
            writer.write(printAdjacencyMatrix(matrixInputWeights));
            writer.write("Dijkstra's: " + dijkstra(matrixInputWeights, STARTING_VERTEX_DIJKSTRA) + "\n");
            writer.close();
        } catch (IOException e) {
            System.out.println("An error occurred.");
            e.printStackTrace();
        }
    }


    //create the adjacency matrix for the file
    private static int[][] createAdjacencyMatrix(List<String> lines, boolean isWeights) {
        //initialize the matrix and size
        int size = lines.size();
        int[][] matrix = new int[size][size];

        //cut off the "a:" that starts each line, leaving just the edges
        //if there's nothing after the "a:", place an empty string
        for (int i=0; i<size; i++) {
            try {
                lines.set(i, lines.get(i).split(":")[1]);
            } catch (Exception e) {
                lines.set(i, "");
            }
        }

        //go one row at a time
        for (int i=0; i<size; i++) {
            //get an array of the edges of this row
            String[] edges = lines.get(i).split(",");
            int[] row = new int[size];

            //convert the edges into an index in the row array
            //if weighted, parse for the weights and use those
            for (String edge : edges) {
                if (isWeights) {
                    try {
                        //elements holds: 0 -> character of the edge, 1 -> weight of the edge
                        String[] elements = edge.split("_");
                        row[(int)elements[0].charAt(0) - (int)'a'] = Integer.parseInt(elements[1]);
                    } catch (Exception e) {}
                }
                else {
                    try {
                        row[(int)edge.charAt(0) - (int)'a'] = 1;
                    } catch (Exception e) {}
                }
            }

            //set the row in the matrix to the row you constructed
            matrix[i] = row;
        }

        //return the filled matrix
        return matrix;
    }

    //return a string of the adjacency matrix
    private static String printAdjacencyMatrix(int[][] matrix) {
        //initialize the size and string
        int size = matrix[0].length;
        String result = "";

        //header row
        String header = "  ";
        for (int i=0; i<size; i++) {
            header += (char)(i + (int)'a') + "";
        }
        result += header + "\n";

        //print each row of the matrix
        for (int i=0; i<size; i++) {
            String row = (char)(i + (int)'a') + " ";
            for (int j=0; j<size; j++) {
                row += matrix[i][j];
            }
            result += row + "\n";
        }

        result += "\n";

        return result;
    }

    //Breadth First Search
    private static String BFS(int[][] matrix, char startVert) {
        //declare/instantiate variables and data structures
        String result = "";
        int size = matrix[0].length;
        //instantiate a queue and enqueue startVert
        Queue<Character> queue = new LinkedList<Character>();
        queue.add(startVert);
        HashMap<Character, Boolean> seenList = new HashMap<Character, Boolean>();
        //fill the hashmap with characters in matrix and false (not yet seen)
        for (int i=0; i<size; i++) {
            seenList.put((char)(i + (int)'a'), false);
        }
        //mark startVert as true (seen)
        seenList.put(startVert, true);

        //loop while there is still items in the queue
        while (!queue.isEmpty()) {
            //dequeue the front item, visit it, add it to result
            char curVert = queue.remove();
            result += curVert + "";
            //for all possible neighbors (the row of this vertex in the matrix), see if each
            //is a valid neighbor and if it's already in the seenList or not
            for (int i=0; i<size; i++) {
                int matrixValue = matrix[(int)curVert - (int)'a'][i];
                char neighbor = (char)(i + (int)'a');
                //if valid neighbor and not in seenList, add to seenList and enqueue it
                if (matrixValue != 0 && seenList.get(neighbor) == false) {
                    seenList.put(neighbor, true);
                    queue.add(neighbor);
                }
            }
        }

        return result;
    }

    //Depth First Search
    private static String DFS(int[][] matrix, char startVert) {
        //declare/instantiate variables and data structures
        String result = "";
        int size = matrix[0].length;
        //instantiate a stack and push startVert
        Stack<Character> stack = new Stack<Character>();
        stack.push(startVert);
        HashMap<Character, Boolean> seenList = new HashMap<Character, Boolean>();
        //fill the hashmap with characters in matrix and false (not yet seen)
        for (int i=0; i<size; i++) {
            seenList.put((char)(i + (int)'a'), false);
        }
        //mark startVert as true (seen)
        seenList.put(startVert, true);

        //loop while there is still items in the stack
        while (!stack.isEmpty()) {
            //pop the top item, visit it, add it to result
            char curVert = stack.pop();
            result += curVert + "";
            //for all possible neighbors (the row of this vertex in the matrix), see if each
            //is a valid neighbor and if it's already in the seenList or not
            for (int i=0; i<size; i++) {
                int matrixValue = matrix[(int)curVert - (int)'a'][i];
                char neighbor = (char)(i + (int)'a');
                //if valid neighbor and not in seenList, add to seenList and push it
                if (matrixValue != 0 && seenList.get(neighbor) == false) {
                    seenList.put(neighbor, true);
                    stack.push(neighbor);
                }
            }
        }

        return result;
    } 

    //Dijkstra's to find shortest path from one vertex to all the others
    private static String dijkstra(int[][] matrix, char startVert) {
        int size = matrix[0].length;
        //holds the shortest path to each vertex from the startVert
        HashMap<Character, Integer> pathLengths = new HashMap<Character, Integer>();
        //holds every character in the matrix, delete a char once it's been visited
        List<Character> unvisited = new ArrayList<Character>();

        for (int i=0; i<size; i++) {
            pathLengths.put((char)(i + (int)'a'), Integer.MAX_VALUE);
            unvisited.add((char)(i + (int)'a'));
        }
        pathLengths.put(startVert, 0);

        char curVert = startVert;
        //loop until all vertices are visited
        while (!unvisited.isEmpty()) {
            //using curVert, go to its row in the matrix and find all its neighbors
            for (int i=0; i<size; i++) {
                int matrixValue = matrix[(int)curVert - (int)'a'][i];
                char vert = (char)(i + (int)'a');
                //if neighbor exists and it's travel length is less than what's currently stored, update path length
                if (matrixValue != 0 && matrixValue + pathLengths.get(curVert) < pathLengths.get(vert) && unvisited.contains(vert)) {
                        pathLengths.put(vert, matrixValue + pathLengths.get(curVert));
                }
            }

            //remove the visited vertex from the visited list
            unvisited.remove(Character.valueOf(curVert));

            //get the next curVert, the shortest unvisited path value from pathLengths table
            int shortestLength = Integer.MAX_VALUE;
            for (int i=0; i<size; i++) {
                char vert = (char)(i + (int)'a');
                if (unvisited.contains(vert) && pathLengths.get(vert) < shortestLength) {
                    shortestLength = pathLengths.get(vert);
                    curVert = vert;
                }
            }
        }

        //create result and return it
        String result = "";
        for (int i=0; i<size; i++) {
            result += (char)(i + (int)'a') + ":" + pathLengths.get((char)(i + (int)'a'));
            if (i != size-1)
                result += ",";
        }
        return result;
    }
}
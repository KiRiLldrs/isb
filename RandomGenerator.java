import java.io.FileWriter;
import java.io.IOException;
import java.util.Random;


public class RandomGenerator {
    public static void getRandomSequence(String filename){
        Random rand = new Random();
        StringBuilder sequence = new StringBuilder();

        for (int i = 0; i < 128; ++i){
            sequence.append(rand.nextInt(2));
        }

        try (FileWriter fileWriter = new FileWriter(filename)){
            fileWriter.write(sequence.toString());
            System.out.println("Sequence was added to file "+filename);
        } catch (IOException e){
            System.err.println("Error when writing to a file:" + e.getMessage());
        }
    };

    public static void main(String[] args){
        getRandomSequence("Random_java.txt");
    };
}
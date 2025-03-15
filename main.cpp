#include <iostream>
#include <random>
#include <string>
#include <fstream>

void getRandomSequence(const std::string& filename) {
	std::random_device rd;
	std::mt19937 gen(rd());
	std::uniform_int_distribution<> dist(0, 1);

	std::string sequence;

	for (int i = 0; i < 128; ++i) {
		sequence += std::to_string(dist(gen));
	}

	std::ofstream file(filename);
	file << sequence;
}

int main() {
	getRandomSequence("Random_cpp.txt");
}
#include <TFile.h>
#include <iostream>

void createProject(const char *filename = "toy_calorimeter_output.root") {
    // Open the ROOT file
    TFile *f = TFile::Open(filename);
    if (!f || f->IsZombie()) {
        std::cerr << "Error: Could not open " << filename << std::endl;
        return;
    }

    // Generate the project
    f->MakeProject("ToyCalorimeter", "*", "recreate++");

    // Close the file
    f->Close();
    std::cout << "Project created in directory: ToyCalorimeter" << std::endl;
}

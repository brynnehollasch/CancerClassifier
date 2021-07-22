# Author: Brynne Hollasch
# Date: March 10, 2020
# Description: Create a classifier that can be used to predict whether a tumor is malignant or benign. Then, ask user to input patient ID
# and if patient ID exists, print that patients record.

###############################################################################
# GLOBAL CONSTANT
# For use as dictionary keys
# You can use this list throughout the program without passing it to a function
# DO NOT MODIFY
ATTRS = []
ATTRS.append("ID")
ATTRS.append("radius")
ATTRS.append("texture")
ATTRS.append("perimeter")
ATTRS.append("area")
ATTRS.append("smoothness")
ATTRS.append("compactness")
ATTRS.append("concavity")
ATTRS.append("concave")
ATTRS.append("symmetry")
ATTRS.append("fractal")
ATTRS.append("class")
###############################################################################


def make_training_set(filename):
    """ Read trainig data from the file whose path is filename.
        Return a list of records, where each record is a dictionary
        containing a value for each of the 12 keys in ATTRS.
    """
    # COMPLETE - DO NOT MODIFY
    training_records = []
    # Read in file
    for line in open(filename,'r'):
        if '#' in line:
            continue
        line = line.strip('\n')
        line_list = line.split(',')
        
        # Create a dictionary for the line and map the attributes in
        # ATTRS to the corresponding values in the line of the file
        record = {}
        
        # read patient ID as an int:
        record[ATTRS[0]] = int(line_list[0].strip())
        
        # read attributes 1 through 10 as floats:
        for i in range(1,11):
            record[ATTRS[i]] = float(line_list[i])
        
        # read the class (label), which is "M", or "B" as a string:
        record[ATTRS[11]] = line_list[31].strip() 

        # Add the dictionary to a list
        training_records.append(record)        

    return training_records


def make_test_set(filename):
    """ Read test data from the file whose path is filename.
        Return a list with the same form as the training
        set, except that each dictionary has an additional
        key "prediction" initialized to "none" that will be
        used to store the label predicted by the classifier. 
    """
    # COMPLETE - DO NOT MODIFY
    test_records = make_training_set(filename)

    for record in test_records:
        record["prediction"] = "none"

    return test_records

def initialize_classifier():
    """ Initialize and return a tumor classifier with values of 0 for each attribute
    """
    return {
        "radius": 0.0,
        "texture": 0.0,
        "perimeter": 0.0,
        "area": 0.0,
        "smoothness": 0.0,
        "compactness": 0.0,
        "concavity": 0.0,
        "concave": 0.0,
        "symmetry": 0.0,
        "fractal": 0.0,
    }

def compute_sums(classifier, record):
    """ Computes sum of each key
        Precondition: classifier must be a dictionary and
                      record must be a number"""
    # for each attribute
    for i in range(1,11):
        # add each attribute from classifier to the attributes from record
        classifier[ATTRS[i]] += record[ATTRS[i]]

def compute_averages(classifier, total):
    """ Computes average of each key
        Precondition: classifier must be a dictionary and
                      total must be a number """
    # for each attribute
    for i in range(1,11):
        # compute average by dividing each attribute by the total 
        classifier[ATTRS[i]] /= total

def compute_midpoints(classifier1, classifier2):
    """ Computes midpoint of each key
        Precondition: classifier1 and classifier2 must be
                      dictionaries """
    # initialize empty dictionary 
    midpoints = {}
    # for each attribute
    for i in range(1,11):
        # midpoint = (classifier1 + classifier2) / 2
        midpoints [ATTRS[i]] = (classifier1[ATTRS[i]] + classifier2[ATTRS[i]]) / 2
        
    return midpoints
        
def train_classifier(training_records):
    """ Return a dict containing the midpoint between averages
        among each class (malignant and benign) of each attribute.
        (See the A5 writeup for a more complete description)
        Precondition: training_records is a list of patient record
                      dictionaries, each of which has the keys
                      in the global variable ATTRS
        Postcondition: the returned dict has midpoint values calculated
                       from the training set for all 10 attributes except
                       "ID" and"class".
    """
    # initialize classifiers and tallies for benign and malignant 
    B_classifier = initialize_classifier()
    M_classifier = initialize_classifier()
    B_total = 0
    M_total = 0
    
    # for each record
    for i in training_records:
        # if the class is benign
        if i['class'] == "B":
            # compute sums of benign cases
            compute_sums(B_classifier, i)
            # add one tally to the total benign tumors
            B_total += 1
        else:
            # compute sums of malignant cases
            compute_sums(M_classifier, i)
            # add one tally to the total malignant tumors
            M_total += 1
     
    #compute averages and midpoints
    compute_averages(B_classifier, B_total)
    compute_averages(M_classifier, M_total)
    midpoints = compute_midpoints(B_classifier, M_classifier)

    return midpoints

def classify(test_records, classifier):
    """ Use the given classifier to make a prediction for each record in
        test_records, a list of dictionary patient records with the keys in
        the global variable ATTRS. A record is classified as malignant
        if at least 5 of the attribute values are above the classifier's
        threshold.
        Precondition: classifier is a dict with midpoint values for all
                      keys in ATTRS except "ID" and "class"
        Postcondition: each record in test_records has the "prediction" key
                       filled in with the predicted class, either "M" or "B"
    """

    # for each test record
    for i in test_records:
        # initialize tallies
        B_total = 0
        M_total = 0
        # for each attribute
        for j in range(1,11):
            # if the current records atrribute is less than or equal to classifiers current attribute,
            if i[ATTRS[j]] <= classifier[ATTRS[j]]:
                # then it is benign. 
                B_total += 1
            # if its greater than,
            else:
                # then it is malignant
                M_total += 1
        # if the number of tallies for malignant is greater than or equal to 5,        
        if M_total >= 5:
            # then predict malignant.
            i["prediction"] = "M"
        # if not,
        else:
            # then predict benign. 
            i["prediction"] = "B"

def report_accuracy(test_records):
    """ Print the accuracy of the predictions made by the classifier
        on the test set as a percentage of correct predictions.
        Precondition: each record in the test set has a "prediction"
        key that maps to the predicted class label ("M" or "B"), as well
        as a "class" key that maps to the true class label. """

    # initialize amount correct
    correct = 0
    # calculate length of the records
    amount_records = len(test_records)
    
    # for each test record
    for i in test_records:
        # if the classifiers prediction is equal to the actual class, add one correct case to tally
        if i['prediction'] == i['class']:
            correct += 1
    
    # convert the amount of correct answers to a percent and print the percent
    correct_percent = 100 * (correct/amount_records)
    print ("Classifier accuracy:" , correct_percent)

def search_records(test_records, patient_ID):
    """Search each record for the ID inputted by the user.
       If found, return the record. If not found, return -1.
       Precondition: patient_ID must be an int"""
    
    # for each test record
    for i in test_records:
        # if the patient ID is found,
        if (i["ID"] == patient_ID):
            # return the record
            return(i)
    # if not found, return -1
    return(-1)

def print_records(patient_record, classifier):
    """Determines whether each attribute is malignant or benign, then
       prints a table of the patients record. """
   
   #initialize the tally
    B_total = 0
    M_total = 0
    
    # print header
    print(("  Attribute        Patient     Classifier            Vote"))
    
    # for each record
    for i in range(1,11):
        # if the current attribute of the pateints record is less than the classifiers current attribute,
        if patient_record[ATTRS[i]] <= classifier[ATTRS[i]]:
            # then predict benign
            prediction = "Benign"
            B_total += 1
        # otherwise,
        else:
            # predict malignant
            prediction = "Malignant"
            M_total += 1
            
        # print the table and format 
        print(ATTRS[i].rjust(11), ("{:.4f}".format(patient_record[ATTRS[i]])).rjust(14),
             ("{:.4f}".format(classifier[ATTRS[i]])).rjust(14), prediction.rjust(15))
        
        # if there are more M's tallied than B's or an equal amount,
        if M_total >= B_total:
            # then the overall diagnosis is malignant.
            overall_prediction = "Malignant"
        # otherwise,
        else:
            # the diagnosis is benign.
            overall_prediction = "Benign"
    
    # print classifiers diagnosis
    print("Classifier's diagnosis: " , overall_prediction)
    
def check_patients(test_records, classifier):
    """ Repeatedly prompt the user for a Patient ID until the user
        enters "quit". For each patient ID entered, search the test
        set for the record with that ID, print a message and prompt
        the user again. If the patient is in the test set, print a
        table: for each attribute, list the name, the patient's value,
        the classifier's midpoint value, and the vote cast by the
        classifier. After the table, output the final prediction made
        by the classifier.
        If the patient ID is not in the test set, print a message and
        repeat the prompt. Assume the user enters an integer or quit
        when prompted for the patient ID.
    """

    # prompt user for an ID
    patient_ID = input("Enter a patient ID to see classification details: ")
    
    # while the user has not entered "quit":
    while patient_ID != "quit":
        # determine whether the entered patient ID is in the test set
        patient_record = search_records(test_records, int(patient_ID))
        # if it is,
        if patient_record != -1:
            # print the record
            print_records(patient_record, classifier)
        # otherwise,
        else:
            # print a message saying the patient ID wasn't found
            print("Patient ID was not found. Try another one.")

        # prompt the user for another ID when done
        patient_ID = input("Enter a patient ID to see classification details: ")

if __name__ == "__main__": 
    # Main program - COMPLETE
    # Do not modify except to uncomment each code block as described.
    
    # load the training set
    print("Reading in training data...")
    training_data_file = "cancerTrainingData.txt"
    training_set = make_training_set(training_data_file)
    print("Done reading training data.")
    
    # load the test set 
    print("Reading in test data...")
    test_file = "cancerTestingData.txt"
    test_set = make_test_set(test_file)
    print("Done reading test data.\n")

    #train the classifier: uncomment this block once you've
    #implemented train_classifier
    print("Training classifier..."    )
    classifier = train_classifier(training_set)
    print("Classifier cutoffs:")
    for key in ATTRS[1:11]:
        print("    ", key, ": ", classifier[key], sep="")
    print("Done training classifier.\n")

    # use the classifier to make predictions on the test set:
    # uncomment the following block once you've written classify
    # and report_accuracy
    print("Making predictions and reporting accuracy")
    classify(test_set, classifier)
    report_accuracy(test_set)
    print("Done classifying.\n")

    # prompt the user for patient IDs and provide details on
    # the diagnosis: uncomment this line when you've
    # implemented check_patients
    check_patients(test_set, classifier)
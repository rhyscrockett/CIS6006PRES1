import tss
from tss import Hash
import base64

import time

import os
import glob
import sys

class TimerException(Exception):
    """A custom exception used to report errors in use of Timer."""

class Timer:
    def __init__(self):
        self.start_time = None
        self.times = list() # store the average of times

    def start(self):
        """Starts a new timer."""
        # check if timer is running
        if self.start_time is not None:
            raise TimerError("Timer is currently running.")

        self.start_time = time.perf_counter() # returns the absolute value of counter

    def stop(self):
        """Stop the timer, and calculate the elapsed time."""
        # check if timer is already running
        if self.start_time is None:
            raise TimerError("Timer is not running.")

        elapsed_time = time.perf_counter() - self.start_time # calculate time taken using current absolute value minus the starting time
        self.start_time = None # set start time back to nil
        print(f"time taken: {elapsed_time:0.4f} seconds.") # print to the 4th decimal place time taken
        self.times.append(elapsed_time) # add the elapsed time to the times list

    def average(self):
        """Return an average time."""
        # check if timer is still running
        if self.start_time is not None:
            raise TimerError("Timer is still running. Must stop() to calculate average.")

        average = sum(self.times) / len(self.times) # the sum of all time divided by the amount of recordings
        print(f"Average time in 10 iterations: {average:0.4f}")

def create_shares(t, s):
    """Use Threshold Secret Sharing (Shamir's Secret Sharing Scheme) to split and encrypt a message."""
    secret = "Hello, I am here for you. Do your best to get closer. There is no reason to live outside the horizon of help."
    share_time = Timer() # create timer for shares
    print() # new line
    print("The secret to be shared:\t", secret) # prints the secret message
    
    print(f"For the combination of {t} storage nodes and {s} shares:")
    for x in range(0, 10):
        share_time.start()
        shares = tss.share_secret(t, s, secret, Hash.NONE) # shamir cipher
        share_time.stop()
    share_time.average()

    print() # new line
    print("The {0} shares created from the secret are: ".format(s)) # print the number of shares
    print("======================================================")
    # for value in the range of 0 to s, create a filename for each share and save he share to that file (STORES EACH SHARE IN A SEPERATE FILE.)
    i = 1 # to set the first share as 1, rather than the index value 0
    for x in range(0, s):
        filename = f"share {i}.txt"
        i += 1 # increment
        f = open(filename, 'wb')
        f.write(shares[x])
        f.close()

    # print each share
    for x in range(0, s):
        print(base64.b64encode(shares[x]))

    print() # new line
    print("Using {0} shares from {1} number of shares to recover the secret".format(t, s))
    print()

def reconstruct_shares(t):
    recover_time = Timer() # create timer for recovery
    shares = []
    # read all shares from each share txt file
    for share in glob.glob("*.txt"):
        print("Found share:")
        with open(os.path.join(os.getcwd(), share), 'rb') as f:
            # gather all shares into one variable
            s = f.read()
            print(base64.b64encode(s))
            shares.append(s)

    # run the recovery time 10 iterations
    for x in range(0, 10):
        recover_time.start()
        reconstructed_secret = tss.reconstruct_secret(shares[0:t]) # build the shares and decrypt message
        recover_time.stop()
    recover_time.average()

    print() # new line
    print("Reconstructed:\t", reconstructed_secret.decode())

def remove_shares():
    while True:
        answer = str(input("Would you like to remove the shares? (y/n): ")).lower().strip()
        if answer == 'y':
            files = glob.glob("*.txt")
            for f in files:
                os.remove(f)
            break
        elif answer == 'n':
            break
        else:
            print("Invalid input.")
            continue

def main():
    try:
        t = int(input("Enter the number of storage nodes to use: ")) # used to adjust storage nodes
        s = int(input("Enter the number of shares to use: ")) # adjust shares
    except ValueError:
        print("Error! Value must be a valid number. Exiting...")
        sys.exit(1)
    create_shares(t, s)
    reconstruct_shares(t)
    remove_shares()
        
if __name__ == '__main__':
    main()

import tobii_research as tr
import time
import csv
import sys
import os

class TobiiWriter(object):
    def __init__(self):
        self.timestr = time.strftime("%Y-%m-%d_%H-%M-%S")
        self.export_fname = f"./tobii_data/{self.timestr}.csv"


        self.header = ["timestamp_computer",
                       "left_gaze_point_on_display_area",
                       "right_gaze_point_on_display_area",
                       "left_pupil_diameter",
                       "right_pupil_validity",
                       "right_pupil_diameter",
                       "right_pupil_validity"]

        self.create_csv_export()
        self.tracker = self.setup_tracker()
        self.subscribe_to_streams(self.tracker)

        while True:
            continue


    def create_csv_export(self):

        if not os.path.exists("./tobii_data/"):
            os.mkdir("./tobii_data/")

        with open (f"{self.export_fname}", "w") as out_csv:
            writer = csv.writer(out_csv, delimiter=",")

            writer.writerow(self.header)


    def write_data_line(self, row):


        with open (f"{self.export_fname}", "a") as out_csv:
            writer = csv.writer(out_csv, delimiter=",")

            writer.writerow(row)


    def gaze_data_callback(self, gaze_data):

        # print(f"Left eye: ({gaze_data['left_gaze_point_on_display_area']}) \t Right eye: ({gaze_data['right_gaze_point_on_display_area']})")
        self.write_data_line([time.time(),
                              gaze_data['left_gaze_point_on_display_area'],
                              gaze_data['right_gaze_point_on_display_area'],
                              gaze_data['left_pupil_diameter'],
                              gaze_data['right_pupil_validity'],
                              gaze_data['right_pupil_diameter'],
                              gaze_data['right_pupil_validity']])


    def setup_tracker(self):

        try:
            trackers = tr.find_all_eyetrackers()
            tracker = trackers[0]
            print(f"Eyetracker: {tracker.model} : Detected! Subscribing to Streams")
            initial_gaze_output_frequency = tracker.get_gaze_output_frequency()
            print(f"Frequency of collection: {initial_gaze_output_frequency} Hz")
        except:
            print("Error in finding tracker... ... ")
            print("Please ensure the tracker is plugged in and calibrated using Eye Tracker Manager!")
            print("Closing program...")
            sys.exit()

        return tracker


    def subscribe_to_streams(self, tracker):

        tracker.subscribe_to(tr.EYETRACKER_GAZE_DATA, self.gaze_data_callback, as_dictionary=True)


if __name__ == "__main__":
    tr = TobiiWriter()

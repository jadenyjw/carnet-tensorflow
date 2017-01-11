import tflearn
from tflearn.data_utils import shuffle
from tflearn.layers.core import input_data, fully_connected
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.estimator import regression
from tflearn.data_preprocessing import ImagePreprocessing
from tflearn.data_augmentation import ImageAugmentation
from tflearn.layers.normalization import local_response_normalization
import h5py
from tflearn.data_utils import build_hdf5_image_dataset

dataset_file = 'train_data.txt'
validation_file = 'cval_data.txt'


build_hdf5_image_dataset(dataset_file, image_shape=[144, 144], mode='file', output_path='dataset.h5', categorical_labels=True)
h5f = h5py.File('dataset.h5', 'r')
X = h5f['X']
Y = h5f['Y']

build_hdf5_image_dataset(validation_file, image_shape=[144, 144], mode='file', output_path='validation.h5', categorical_labels=True)

h5f = h5py.File('validation.h5', 'r')
X_val = h5f['X']
Y_val = h5f['Y']

X, Y = shuffle(X, Y)

# Make sure the data is normalized
img_prep = ImagePreprocessing()
img_prep.add_featurewise_zero_center()
img_prep.add_featurewise_stdnorm()

# Create extra synthetic training data by flipping, rotating and blurring the
# images on our data set.

# Define our network architecture:

# Input is a 32x32 image with 3 color channels (red, green and blue)
network = input_data(shape=[None, 144, 144, 3],
                     data_preprocessing=img_prep)


# Step 1: Convolution

network = fully_connected(network, 64, activation='relu')

network = fully_connected(network, 3, activation='softmax')


# Tell tflearn how we want to train the network
network = regression(network, optimizer='adam',
                     loss='categorical_crossentropy',
                     learning_rate=0.001)

# Wrap the network in a model object
model = tflearn.DNN(network, tensorboard_verbose=0, checkpoint_path='carnet.tfl.ckpt')

# Train it! We'll do 100 training passes and monitor it as it goes.
model.fit(X, Y, n_epoch=100, shuffle=True, validation_set=(X_val, Y_val),
          show_metric=True,
          snapshot_epoch=True,
          run_id='carnet')

# Save model when training is complete to a file
model.save("carnet.tfl")
print("Network trained and saved as carnet.tfl!")

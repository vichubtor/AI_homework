
#MNIST

import tensorflow as tf
import numpy as np
from tensorflow.examples.tutorials.mnist import input_data
'''
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

acc = np.array([])
'''
mnist = input_data.read_data_sets('./',one_hot=True)

def add_layer(inputs,in_size,out_size,n_layer,activation_function=None):
    layer_name = 'layer%s' % n_layer
    with tf.name_scope(layer_name):
        #first define weight & bias
        with tf.name_scope('weights'):
            Weights = tf.Variable(tf.random_normal([in_size,out_size]))
            tf.summary.histogram(layer_name+'/weights',Weights)
        with tf.name_scope('biases'):
            biases = tf.Variable(tf.zeros([1,out_size])+0.1)
            tf.summary.histogram(layer_name+'/biases',biases)
        with tf.name_scope('Wx_plus_b'):
            Wx_plus_b = tf.matmul(inputs,Weights) + biases
            tf.summary.histogram(layer_name+'/Wx_plus_b',Wx_plus_b)
        
        if activation_function is None:
            outputs = Wx_plus_b
        else:
            outputs = activation_function(Wx_plus_b)
        tf.summary.histogram(layer_name+'/outputs',outputs)
        return outputs

def compute_accuracy(v_xs,v_ys):
    global prediction
    y_pre = sess.run(prediction,feed_dict={xs:v_xs})
    correct_prediction = tf.equal(tf.argmax(y_pre,1),tf.argmax(v_ys,1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction,tf.float32))
    result = sess.run(accuracy,feed_dict={xs:v_xs,ys:v_ys})
    return result

with tf.name_scope('inputs'):
    xs = tf.placeholder(tf.float32,[None,784])
    ys = tf.placeholder(tf.float32,[None,10])

with tf.name_scope('prediction'):
    prediction = add_layer(xs,784,10,1,activation_function=tf.nn.softmax)

with tf.name_scope('cross_entropy'):
    cross_entropy = tf.reduce_mean(-tf.reduce_sum(ys * tf.log(prediction),reduction_indices=[1]))
    tf.summary.scalar('cross_entropy',cross_entropy)

train_step = tf.train.GradientDescentOptimizer(0.4).minimize(cross_entropy)

sess = tf.Session()

merged = tf.summary.merge_all()

writer = tf.summary.FileWriter("./",sess.graph)

sess.run(tf.global_variables_initializer())

for i in range(1000):
    batch_xs,batch_ys = mnist.train.next_batch(100)
    sess.run(train_step,feed_dict={xs:batch_xs,ys:batch_ys})

    if i % 50 == 0:
        result = sess.run(merged,feed_dict={xs:batch_xs,ys:batch_ys})
        writer.add_summary(result,i)
        print(compute_accuracy(mnist.test.images,mnist.test.labels))
        




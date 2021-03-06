#!/usr/bin/env python
from __future__ import print_function
import argparse
import random

import numpy as np
import pandas as pd

import chainer
from chainer import training
from chainer.training import extensions

import densenet


class LabelDataset(chainer.dataset.dataset_mixin.DatasetMixin):
    def __init__(self, paths, dtype=np.float32):
        df = pd.read_csv(paths)
        df = df.drop("Unnamed: 0", axis=1)
        self._paths = df
        self._dtype = dtype
    def __len__(self):
        return len(self._paths)
    def get_example(self, i):
        return np.array(self._paths.ix[i, :].tolist(), dtype = np.int32)

class PreprocessedDataset(chainer.dataset.DatasetMixin):

    def __init__(self, path, root, label, crop_size, random=True):
        self.image = chainer.datasets.ImageDataset(path, root)
        self.label = LabelDataset(label)
        self.crop_size = crop_size
        self.random = random

    def __len__(self):
        return len(self.image)

    def get_example(self, i):
        # It reads the i-th image/label pair and return a preprocessed image.
        # It applies following preprocesses:
        #     - Cropping (random or center rectangular)
        #     - Random flip
        #     - Scaling to [0, 1] value
        crop_size = self.crop_size

        image = self.image[i]
        label = self.label[i]
        _, h, w = image.shape

        if self.random:
            # Randomly crop a region and flip the image
            top = random.randint(0, h - crop_size - 1)
            left = random.randint(0, w - crop_size - 1)
            if random.randint(0, 1):
                image = image[:, :, ::-1]
        else:
            # Crop the center
            top = (h - crop_size) // 2
            left = (w - crop_size) // 2
        bottom = top + crop_size
        right = left + crop_size

        image = image[:, top:bottom, left:right]
        #image -= self.mean[:, top:bottom, left:right]
        image /= 255
        return image, label


class TestModeEvaluator(extensions.Evaluator):

    def evaluate(self):
        model = self.get_target('main')
        model.train = False
        ret = super(TestModeEvaluator, self).evaluate()
        model.train = True
        return ret


def main():
    archs = {
           'densenet': densenet.DenseNet
    }

    parser = argparse.ArgumentParser(
        description='Learning convnet from ILSVRC2012 dataset')
    parser.add_argument('train', help='Path to training image list file')
    parser.add_argument('trainlabel', help='Path to training label list file')
    parser.add_argument('val', help='Path to validation image list file')
    parser.add_argument('vallabel', help='Path to validation label list file')
    parser.add_argument('--arch', '-a', choices=archs.keys(), default='densenet',
                        help='Convnet architecture')
    parser.add_argument('--batchsize', '-B', type=int, default=32,
                        help='Learning minibatch size')
    parser.add_argument('--epoch', '-E', type=int, default=600,
                        help='Number of epochs to train')
    parser.add_argument('--gpu', '-g', type=int, default=-1,
                        help='GPU ID (negative value indicates CPU')
    parser.add_argument('--initmodel',
                        help='Initialize the model from given file')
    parser.add_argument('--loaderjob', '-j', type=int,
                        help='Number of parallel data loading processes')
    #parser.add_argument('--mean', '-m', default='mean.npy',
    #                    help='Mean file (computed by compute_mean.py)')
    parser.add_argument('--resume', '-r', default='',
                        help='Initialize the trainer from given file')
    parser.add_argument('--out', '-o', default='result',
                        help='Output directory')
    parser.add_argument('--root', '-R', default='.',
                        help='Root directory path of image files')
    parser.add_argument('--val_batchsize', '-b', type=int, default=250,
                        help='Validation minibatch size')
    parser.add_argument('--test', action='store_true')
    parser.set_defaults(test=False)
    args = parser.parse_args()

    # Initialize the model to train
    model = archs[args.arch]()
    if args.initmodel:
        print('Load model from', args.initmodel)
        chainer.serializers.load_npz(args.initmodel, model)
    if args.gpu >= 0:
        chainer.cuda.get_device(args.gpu).use()  # Make the GPU current
        model.to_gpu()

    # Load the datasets and mean file
    #mean = np.load(args.mean)
    train = PreprocessedDataset(args.train, args.root, args.trainlabel, model.insize)
    val = PreprocessedDataset(args.val, args.root, args.vallabel, model.insize, False)
    # These iterators load the images with subprocesses running in parallel to
    # the training/validation.
    train_iter = chainer.iterators.MultiprocessIterator(
        train, args.batchsize, n_processes=args.loaderjob)
    val_iter = chainer.iterators.MultiprocessIterator(
        val, args.val_batchsize, repeat=False, n_processes=args.loaderjob)

    # Set up an optimizer
    optimizer = chainer.optimizers.Adam(alpha=0.0005, beta1=0.9, beta2=0.999, eps=1e-08)
    optimizer.setup(model)

    # Set up a trainer
    updater = training.StandardUpdater(train_iter, optimizer, device=args.gpu)
    trainer = training.Trainer(updater, (args.epoch, 'epoch'), args.out)

    val_interval = (10 if args.test else 20), 'iteration'
    log_interval = (10 if args.test else 10), 'iteration'

    trainer.extend(TestModeEvaluator(val_iter, model, device=args.gpu),
                   trigger=val_interval)
    trainer.extend(extensions.dump_graph('main/loss'))
    trainer.extend(extensions.snapshot(), trigger=(20,'epoch'))
    trainer.extend(extensions.snapshot_object(
        model, 'model_iter_{.updater.iteration}'), trigger=(20,'epoch'))
    # Be careful to pass the interval directly to LogReport
    # (it determines when to emit log rather than when to read observations)
    trainer.extend(extensions.LogReport(trigger=log_interval))
    trainer.extend(extensions.observe_lr(), trigger=log_interval)
    trainer.extend(extensions.PrintReport([
        'epoch', 'iteration', 'main/loss', 'validation/main/loss',
        'main/accuracy', 'validation/main/accuracy', 'lr'
    ]), trigger=log_interval)
    trainer.extend(extensions.ProgressBar(update_interval=10))

    if args.resume:
        chainer.serializers.load_npz(args.resume, trainer)

    trainer.run()


if __name__ == '__main__':
    main()

import chainer
import chainer.functions as F
import numpy as np
from chainer import cuda
from chainer import function
from chainer.utils import type_check


class MyAccuracy(function.Function):

    def check_type_forward(self, in_types):
        type_check.expect(in_types.size() == 2)
        x_type, t_type = in_types

        type_check.expect(
            x_type.dtype == np.float32,
            t_type.dtype == np.int32,
            x_type.shape == t_type.shape
        )
        
    def forward(self, inputs):
        xp = cuda.get_array_module(*inputs)
        y, t = inputs
        
        mask1 = (y>0.5)
        
        y2= xp.zeros(y.size,dtype=np.float32).reshape(y.shape)
        y2= xp.where(mask1, 1, y2)        
        
        acc = ((y2==1)&(t==1)).sum()/t.sum()

        return xp.asarray(acc),

def myaccuracy(y, t):
    
    return MyAccuracy()(y, t)

class DenseBlock(chainer.Chain):
    def __init__(self, in_ch, growth_rate, n_layer):
        self.dtype = np.float32
        self.n_layer = n_layer
        super(DenseBlock, self).__init__()
        for i in moves.range(self.n_layer):
            W = initializers.HeNormal(1 / np.sqrt(2), self.dtype)
            self.add_link('bn{}'.format(i + 1),
                          L.BatchNormalization(in_ch + i * growth_rate))
            self.add_link('conv{}'.format(i + 1),
                          L.Convolution2D(in_ch + i * growth_rate,
                                          growth_rate, 3, 1, 1, initialW=W))

    def __call__(self, x, dropout_ratio, train):
        for i in moves.range(1, self.n_layer + 1):
            h = F.relu(self['bn{}'.format(i)](x, test = not train))
            h = F.dropout(self['conv{}'.format(i)](h), dropout_ratio, train)
            x = F.concat((x, h))
        return x

class Transition(chainer.Chain):
    def __init__(self, in_ch):
        self.dtype = np.float32
        W = initializers.HeNormal(1 / np.sqrt(2), self.dtype)
        super(Transition, self).__init__(
            bn=L.BatchNormalization(in_ch),
            conv=L.Convolution2D(in_ch, in_ch, 1, initialW=W))

    def __call__(self, x, dropout_ratio, train):
        h = F.relu(self.bn(x, test=not train))
        h = F.dropout(self.conv(h), dropout_ratio, train)
        h = F.average_pooling_2d(h, 2)
        return h


class DenseNet(chainer.Chain):
    def __init__(self, n_layer=12, growth_rate=12,
                 n_class=10, dropout_ratio=0.2, in_ch=16, block=3):
        
        """DenseNet definition.
        Args:
            n_layer: Number of convolution layers in one dense block.
                If n_layer=12, the network is made out of 40 (12*3+4) layers.
                If n_layer=32, the network is made out of 100 (32*3+4) layers.
            growth_rate: Number of output feature maps of each convolution
                layer in dense blocks, which is difined as k in the paper.
            n_class: Output class.
            dropout_ratio: Dropout ratio.
            in_ch: Number of output feature maps of first convolution layer.
            block: Number of dense block.
        """

        self.dtype = np.float32
        self.insize = 32
        self.dropout_ratio = dropout_ratio
        in_chs = moves.range(
            in_ch, in_ch + (block + 1) * n_layer * growth_rate,
            n_layer * growth_rate)
        W = initializers.HeNormal(1 / np.sqrt(2), self.dtype)

        super(DenseNet, self).__init__()
        self.add_link('conv1', L.Convolution2D(3, in_ch, 3, 1, 1, initialW=W))
        for i in moves.range(block):
            self.add_link('dense{}'.format(i + 2),
                          DenseBlock(in_chs[i], growth_rate, n_layer))
            if not i == block - 1:
                self.add_link('trans{}'.format(i + 2), Transition(in_chs[i + 1]))
        self.add_link(
            'bn{}'.format(block + 1), L.BatchNormalization(in_chs[block]))
        self.add_link('fc{}'.format(block + 2), L.Linear(7168, n_class))

        self.train = True
        self.dropout_ratio = dropout_ratio
        self.block = block

    def __call__(self, x, t):
        h = self.conv1(x)
        for i in moves.range(2, self.block + 2):
            h = self['dense{}'.format(i)](h , self.dropout_ratio, self.train)
            if not i == self.block + 1:
                h = self['trans{}'.format(i)](h, self.dropout_ratio, self.train)
        h = F.relu(self['bn{}'.format(self.block + 1)](h, test=not self.train))
        h = F.average_pooling_2d(h, int(h.data.shape[2]/4))
        h = F.reshape(h, (h.data.shape[0], 7168))
        h = self['fc{}'.format(self.block + 2)](h)

        loss = F.sigmoid_cross_entropy(h, t)
        chainer.report({'loss': loss, 'accuracy': myaccuracy(h, t)}, self)
        return loss

    def inspection(self, x):
        h = self.conv1(x)
        for i in moves.range(2, self.block + 2):
            h = self['dense{}'.format(i)](h , self.dropout_ratio, False)
            if not i == self.block + 1:
                h = self['trans{}'.format(i)](h, self.dropout_ratio, False)
        h = F.relu(self['bn{}'.format(self.block + 1)](h, test=True))
        h = F.average_pooling_2d(h, int(h.data.shape[2]/4))
        h = F.reshape(h, (h.data.shape[0], 7168))
        h = self['fc{}'.format(self.block + 2)](h)
        h = F.sigmoid(h)
        return h

    
    def tovec_binary(self, x):
        h = self.conv1(x)
        for i in moves.range(2, self.block + 2):
            h = self['dense{}'.format(i)](h , self.dropout_ratio, False)
            if not i == self.block + 1:
                h = self['trans{}'.format(i)](h, self.dropout_ratio, False)
        h = F.relu(self['bn{}'.format(self.block + 1)](h, test=True))
        h = F.average_pooling_2d(h, int(h.data.shape[2]/4))
        h = F.reshape(h, (h.data.shape[0], 7168))
        h = F.sigmoid(h)
        mask = (h.data>0.5)        
        h2= np.zeros(h.data.size,dtype=np.float32).reshape(h.data.shape)
        h2= np.where(mask, 1, h2)
        return h2

    def tovec_real(self, x):
        h = self.conv1(x)
        for i in moves.range(2, self.block + 2):
            h = self['dense{}'.format(i)](h , self.dropout_ratio, False)
            if not i == self.block + 1:
                h = self['trans{}'.format(i)](h, self.dropout_ratio, False)
        h = F.relu(self['bn{}'.format(self.block + 1)](h, test=True))
        h = F.average_pooling_2d(h, int(h.data.shape[2]/4))
        h = F.reshape(h, (h.data.shape[0], 7168))
        return h.data

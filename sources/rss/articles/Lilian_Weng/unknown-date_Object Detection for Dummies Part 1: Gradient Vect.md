# Object Detection for Dummies Part 1: Gradient Vector, HOG, and SS

> 来源: Lilian Weng  
> 发布时间: Sun, 29 Oct 2017 00:00:00 +0000  
> 分类: 海外技术领袖  
> 优先级: high

## 摘要

<!-- In this series of posts on "Object Detection for Dummies", we will go through several basic concepts, algorithms, and popular deep learning models for image processing and objection detection. Hopefully, it would be a good read for people with no experience in this field but want to learn more. The Part 1 introduces the concept of Gradient Vectors, the HOG (Histogram of Oriented Gradients) algorithm, and Selective Search for image segmentation. -->
<p>I&rsquo;ve never worked in the field of computer vision and has no idea how the magic could work when an autonomous car is configured to tell apart a stop sign from a pedestrian in a red hat. To motivate myself to look into the maths behind object recognition and detection algorithms, I&rsquo;m writing a few posts on this topic &ldquo;Object Detection for Dummies&rdquo;. This post, part 1, starts with super rudimentary concepts in image processing and a few methods for image segmentation. Nothing related to deep neural networks yet. Deep learning models for object detection and recognition will be discussed in <a href="https://lilianweng.github.io/posts/2017-12-15-object-recognition-part-2/">Part 2</a> and <a href="https://lilianweng.github.io/posts/2017-12-31-object-recognition-part-3/">Part 3</a>.</p>

## 链接

https://lilianweng.github.io/posts/2017-10-29-object-recognition-part-1/

---

*ID: e5ceab467697e81d*
*抓取时间: 2026-03-05T10:01:44.823922*

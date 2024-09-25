#include <linux/cdev.h>
#include <linux/fs.h>
#include <linux/kernel.h>
#include <linux/module.h>
#include <linux/slab.h>
#include <linux/uaccess.h>

MODULE_LICENSE("GPL");
MODULE_AUTHOR("ptr-yudai");
MODULE_DESCRIPTION("kbuf - Beginners CTF 2024");

#define DEVICE_NAME "kbuf"
#define MEMO_SIZE 0x800

static struct kmem_cache *kbuf_cache = NULL;

static int module_open(struct inode *inode,
                       struct file *filp) {
  filp->private_data = kmem_cache_alloc(kbuf_cache, GFP_KERNEL);
  return filp->private_data ? 0 : -ENOMEM;
}

static int module_close(struct inode *inode,
                        struct file *filp) {
  kmem_cache_free(kbuf_cache, filp->private_data);
  return 0;
}

static ssize_t module_read(struct file *filp,
                           char __user *buf,
                           size_t size,
                           loff_t *pos) {
  if (copy_to_user(buf, filp->private_data + *pos, size))
    return -EINVAL;

  *pos += size;
  return size;
}

static ssize_t module_write(struct file *filp,
                            const char __user *buf,
                            size_t size,
                            loff_t *pos) {
  if (copy_from_user(filp->private_data + *pos, buf, size))
    return -EINVAL;

  *pos += size;
  return size;
}

static loff_t module_lseek(struct file *filp,
                           loff_t offset,
                           int orig) {
  loff_t new_pos = 0;

  switch (orig) {
    case 0: // SEEK_SET
      new_pos = offset;
      break;
    case 1: // SEEK_CUR
      new_pos = filp->f_pos + offset;
      break;
    case 2: // SEEK_END
      new_pos = MEMO_SIZE + offset;
      break;
  }

  return filp->f_pos = new_pos;
}

static struct file_operations module_fops = {
  .owner   = THIS_MODULE,
  .open    = module_open,
  .release = module_close,
  .read    = module_read,
  .write   = module_write,
  .llseek  = module_lseek,
};

static dev_t dev_id;
static struct cdev c_dev;

static int __init module_initialize(void)
{
  kbuf_cache = kmem_cache_create("kbuf_cache", MEMO_SIZE, 0, SLAB_HWCACHE_ALIGN, NULL);
  if (!kbuf_cache)
    return -ENOMEM;

  if (alloc_chrdev_region(&dev_id, 0, 1, DEVICE_NAME))
    return -EBUSY;

  cdev_init(&c_dev, &module_fops);
  c_dev.owner = THIS_MODULE;

  if (cdev_add(&c_dev, dev_id, 1)) {
    unregister_chrdev_region(dev_id, 1);
    return -EBUSY;
  }

  return 0;
}

static void __exit module_cleanup(void)
{
  if (kbuf_cache)
    kmem_cache_destroy(kbuf_cache);

  cdev_del(&c_dev);
  unregister_chrdev_region(dev_id, 1);
}

module_init(module_initialize);
module_exit(module_cleanup);

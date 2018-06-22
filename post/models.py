from django.db import models
from user.models import User


class Post(models.Model):
	uid = models.IntegerField()
	title = models.CharField(max_length=64)
	created = models.DateTimeField(auto_now_add=True)
	content = models.TextField()

	@property
	def auth(self):
		if not hasattr(self, '_auth'):
			self._auth = User.objects.get(id=self.uid)
		return self._auth

	def comments(self):
		return Comment.objects.filter(post_id=self.id).order_by('-created')

	@property
	def tags(self):
		'''获取旧标签'''

		relations = Relations.objects.filter(post_id=self.id).only('tag_id')
		tag_id_list = [r.tag_id for r in relations]
		return Tag.objects.filter(id__in=tag_id_list)

	def update_tags(self,tag_names):
		'''更新帖子与标签的关系'''

		tag_names = set(tag_names)  # 修改后的标签
		Tag.ensure_tag_name(tag_names)  # 确保传入的tag name 在tag表中存在

		# 获取旧标签
		old_tags = self.tags
		old_tag_names = set(t.name for t in old_tags)
		
		# 创建与新Tags的关系
		need_add_relation_tag_names = tag_names - old_tag_names  # 得到需要新建立的关系
		Relations.add_post_tags(self.id, need_add_relation_tag_names)  # 给后来添加的标签创建新的关系

		# 删除不存在的关系
		need_del_relation_tag_names = old_tag_names - tag_names  # 得到需要丢弃的旧关系
		Relations.del_post_tags(self.id, need_del_relation_tag_names)  		# 


class Comment(models.Model):
	uid = models.IntegerField()
	post_id = models.IntegerField()
	created = models.DateTimeField(auto_now_add=True)
	content = models.TextField()

	@property
	def user(self):
		if not hasattr(self, '_user'):
			self._user = User.objects.get(id=self.uid)
		return self._user

	@property
	def post(self):
		if not hasattr(self, '_post'):
			self._post = User.objects.get(id=self.post_id)
		return self._post


class Tag(models.Model):
	name = models.CharField(max_length=100)

	@classmethod
	def ensure_tag_name(cls,tag_names):
		'''确保Tag中有标签'''

		exist_tags = cls.objects.filter(name__in=tag_names)
		exist_tag_names = [t.name for t in exist_tags]
		need_create_names = [name for name in tag_names if name not in exist_tag_names]

		# 创建原来没有的标签
		if need_create_names:			
			need_create_tags = [cls(name=name) for name in need_create_names]
			cls.objects.bulk_create(need_create_tags)


class Relations(models.Model):
	tag_id = models.IntegerField()
	post_id = models.IntegerField()

	# @classmethod
	# def add_relations(cls):
	# 	cls.objects.cretae(post_id=post_id,tag_id=tag_id)
		
	# @classmethod
	# def del_relations(cls):
	# 	cls.objects.get(post_id=post_id,tag_id=tag_id).delete()

	@classmethod
	def add_post_tags(cls,post_id,tag_names):
		'''批量创建关系'''

		tags = Tag.objects.filter(name__in=tag_names).only('id')
		tag_id_list = [t.id for t in tags]
		need_create_relations = [cls(post_id=post_id,tag_id=tid) for tid in tag_id_list]
		cls.objects.bulk_create(need_create_relations)

	@classmethod
	def del_post_tags(cls,post_id,tag_names):
		'''批量删除关系'''

		tags = Tag.objects.filter(name__in=tag_names).only('id')
		tag_id_list = [t.id for t in tags]
		cls.objects.filter(post_id=post_id, tag_id__in=tag_id_list).delete()







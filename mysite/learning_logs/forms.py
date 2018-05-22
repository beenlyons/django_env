from django import forms
from .models import Topic, Entry

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic # 根据Topic这个model创建表单
        fields = ['text']    # 包含的字段
        labels = {"text": ''} # 不要让django为text生成标签


class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['text']
        labels = {"text": ""}
        # widget小部件，是一个表单元素，如单行文本框，多行文本区域或者下拉列表，这里是用多行文本框，默认为40列，这里改成80
        widgets = {"text": forms.Textarea(attrs={"cols": 80})}

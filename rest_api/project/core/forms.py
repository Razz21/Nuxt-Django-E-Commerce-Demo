from django import forms
from .models import ItemColor, Item
from django.utils.safestring import mark_safe


class MultipleImagesForm(forms.ModelForm):
    image = forms.ImageField(widget=forms.ClearableFileInput(attrs={"multiple": True}))


class ColorTextField(forms.widgets.TextInput):
    def render(self, name, value, attrs=None, renderer=None):
        rendered = super().render(name, value, attrs, renderer)
        inline_code = mark_safe(
            f"""
        <input type="color" value="{value}"/>

        <script type="text/javascript">
            (function(){{
                var form_field = document.querySelector('.field-{name}')
                var text_input = form_field.querySelector('input[name={name}]')
                var color_picker = form_field.querySelector('input[type=color]')

                text_input.addEventListener('input', e=> {{color_picker.value = e.target.value}})
                color_picker.addEventListener('change', e=> {{text_input.value = e.target.value}})
            }})();
        </script>

        """
        )
        return rendered + inline_code


class SelectColorPreview(forms.widgets.Select):
    def render(self, name, value, attrs=None, renderer=None):
        rendered = super().render(name, value, attrs, renderer)
        inline_code = mark_safe(
            f"""
        <div style="height:20px;width:20px;display:inline-block;margin:0 10px" id="select-preview"></div>

        <script type="text/javascript">
            (function(){{
                var form_field = document.querySelector('.field-{name}')
                var select = form_field.querySelector('select')
                var preview = form_field.querySelector('#select-preview')

                select.addEventListener('change', e => {{
                    const optionText = e.target.options[e.target.selectedIndex].text.split('-')
                    preview.style.backgroundColor = optionText[optionText.length-1]
                }})
                
            }})();
        </script>
        <style>
            .field-{name} .related-widget-wrapper{{
                display:flex;
                align-items:center;
            }}
        </style>
        """
        )
        return rendered + inline_code


class ItemColorForm(forms.ModelForm):
    class Meta:
        model = ItemColor
        fields = ("name", "hex")
        widgets = {"hex": ColorTextField()}


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = "__all__"
        widgets = {"color": SelectColorPreview()}

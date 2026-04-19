<div align="center">
<img width="120" style="padding-top: 50px; margin: 0;" src="https://github.com/wenlng/git-assets/blob/master/go-captcha/gocaptcha_logo.svg?raw=true"/>
<h1 style="margin: 0; padding: 0">PyCaptcha</h1>
<p>Python 行为验证码</p>
<a href="https://pypi.org/project/py-captcha/"><img src="https://img.shields.io/pypi/v/py-captcha.svg"/></a>
<a href="https://pypi.org/project/py-captcha/"><img src="https://img.shields.io/pypi/pyversions/py-captcha.svg"/></a>
<a href="https://github.com/wenlng/py-captcha/releases"><img src="https://img.shields.io/github/v/release/wenlng/py-captcha.svg"/></a>
<a href="https://github.com/wenlng/py-captcha/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-Apache2.0-green.svg"/></a>
<a href="https://github.com/wenlng/py-captcha"><img src="https://img.shields.io/github/stars/wenlng/py-captcha.svg"/></a>
<a href="https://github.com/wenlng/py-captcha"><img src="https://img.shields.io/github/last-commit/wenlng/py-captcha.svg"/></a>
</div>

<br/>

> [English](README.md) | 中文

<p style="text-align: center">
<a style="font-weight: bold" href="https://github.com/wenlng/py-captcha">PyCaptcha</a> 是功能强大、模块化且高度可定制的行为式验证码库，支持多种交互式验证码类型：点选（Click）、滑动（Slide）、拖拽（Drag-Drop） 和 旋转（Rotate）。
</p>

<p style="text-align: center"> ⭐️ 如果能帮助到你，请随手给点一个star</p>

<br/>

<div align="center">
<img src="https://github.com/wenlng/git-assets/blob/master/go-captcha/go-captcha-v2.jpg?raw=true" alt="Poster">
</div>

<br/>
<hr/>
<br/>

## 项目生态

| 名称                                                                         | 描述                                                                                          |
|----------------------------------------------------------------------------|---------------------------------------------------------------------------------------------|
| [document](http://gocaptcha.wencodes.com)                                  | Captcha 文档                                                                                  |
| [online demo](http://gocaptcha.wencodes.com/demo/)                         | Captcha 在线演示                                                                                |
| [py-captcha](https://github.com/wenlng/py-captcha)                         | Python 验证码                                                                                  |
| [go-captcha](https://github.com/wenlng/go-captcha)                         | Golang 验证码                                                                                  |
| [next-captcha](https://github.com/wenlng/next-captcha)                     | Node.js 验证码                                                                                 |
| [go-captcha-example](https://github.com/wenlng/go-captcha-example)         | Golang + 前端 + APP实例                                                                         |
| [go-captcha-assets](https://github.com/wenlng/go-captcha-assets)           | Golang 内嵌素材资源                                                                               |
| [go-captcha-jslib](https://github.com/wenlng/go-captcha-jslib)             | Javascript 验证码                                                                              |
| [go-captcha-vue](https://github.com/wenlng/go-captcha-vue)                 | Vue 验证码                                                                                     |
| [go-captcha-react](https://github.com/wenlng/go-captcha-react)             | React 验证码                                                                                   |
| [go-captcha-angular](https://github.com/wenlng/go-captcha-angular)         | Angular 验证码                                                                                 |
| [go-captcha-svelte](https://github.com/wenlng/go-captcha-svelte)           | Svelte 验证码                                                                                  |
| [go-captcha-solid](https://github.com/wenlng/go-captcha-solid)             | Solid 验证码                                                                                   |
| [go-captcha-uni](https://github.com/wenlng/go-captcha-uni)                 | UniApp 验证码，兼容 App、小程序、快应用等                                                                  |
| [go-captcha-flutter](https://github.com/wenlng/go-captcha-flutter)         | Flutter 验证码                                                                                 |
| [go-captcha-service](https://github.com/wenlng/go-captcha-service)         | GoCaptcha 服务，支持二进制、Docker镜像等方式部署，<br/> 提供 HTTP/GRPC 方式访问接口，<br/>可用单机模式和分布式（服务发现、负载均衡、动态配置等） |
| [go-captcha-service-sdk](https://github.com/wenlng/go-captcha-service-sdk) | GoCaptcha 服务SDK工具包，包含 HTTP/GRPC 请求服务接口，<br/>支持静态模式、服务发现、负载均衡                                |
| ...                                                                        |                                                                                             |

<br/>

## 核心特性

- **多样化验证码类型**：支持点选、滑动、旋转和拖拽四种行为式验证码，适应不同交互场景。
- **高度可定制化**：通过选项（`Options`）和资源（`Resources`）支持图像、字体、颜色、角度、大小等灵活配置。
- **高级图像处理**：内置动态图像生成和处理功能，支持主图像、缩略图、拼图块和阴影效果的生成。
- **模块化架构**：代码结构清晰，遵循 Python 语言最佳实践，易于扩展和维护。
- **高性能设计**：优化资源管理和图像生成，适合高并发场景。
- **跨平台兼容**：生成的验证码图像可无缝集成到 Web 应用、移动应用或其他需要验证码的系统。

<br/>

## 验证码类型

`py-captcha` 支持以下四种验证码类型，每种类型具有独特的交互方式、生成逻辑和应用场景：

1. **点选验证码（Click）**：用户在主图像中点击指定的点或字符，支持文本模式和图形模式。
2. **滑动验证码（Slide）**：用户将拼图块滑动到主图像中的正确位置，支持基本模式和拖拽模式。
3. **拖拽验证码（DragDrop）**：滑动验证码的变体，允许用户在更大范围内拖动拼图块到目标位置。
4. **旋转验证码（Rotate）**：用户旋转缩略图使其与主图像的角度对齐。

<br/>

## 安装

```shell
$ pip install py-captcha
```

## 导入模块

```python
from py_captcha import ClickBuilder, SlideBuilder, RotateBuilder

# 或者按需导入特定模块
from py_captcha.click import ClickBuilder
from py_captcha.slide import SlideBuilder
from py_captcha.rotate import RotateBuilder
```

<br />

## 🖖 点选验证码（Click）

点选验证码要求用户在主图像中点击指定的点或字符，适合需要快速验证的场景。支持两种模式：

- **文本模式**：显示字符（如字母、数字或中文），用户点击对应字符。
- **图形模式**：显示图形（如图标或形状），用户点击对应图形。

### 工作原理

1. **生成主图像**（`master_image`）：包含随机分布的点或字符，通常为 JPEG 格式。
2. **生成缩略图**（`thumb_image`）：显示需要点击的目标点或字符，通常为 PNG 格式。
3. **用户交互**：用户点击主图像中的坐标，前端捕获坐标并发送到后端。
4. **验证逻辑**：后端比较用户点击的坐标与目标点（`dots`）的坐标是否匹配。

### 代码示例

```python
from py_captcha import ClickBuilder
from py_captcha.base import option
from PIL import Image

# 创建构建器
builder = ClickBuilder(
    range_len=option.RangeVal(min=4, max=6),
    range_verify_len=option.RangeVal(min=2, max=4),
)

# 加载资源
fonts = ['path/to/font.ttf']
backgrounds = [Image.open('path/to/bg.jpg')]

# 设置资源
builder.set_resources(
    chars=['这', '是', '随', '机', '的', '文', '本', '种', '子'],
    fonts=fonts,
    backgrounds=backgrounds,
)

# 生成验证码
captcha = builder.make()
capt_data = captcha.generate()

# 获取数据
dots = capt_data.get_data()
master_image = capt_data.get_master_image()
thumb_image = capt_data.get_thumb_image()

# 转换为 Base64
master_base64 = master_image.to_base64()
thumb_base64 = thumb_image.to_base64()

print(f"点位信息: {dots}")
print(f"主图: {master_base64}")
print(f"缩略图: {thumb_base64}")
```

### 创建实例
- `builder.make()` - 文本模式（文本/字母数字点选）
- `builder.make_shape()` - 图形模式（图形点选）

### 配置选项
> `ClickBuilder(option_name=value, ...)` 或 `builder.set_options(option_name=value, ...)`

| Options                                    | Desc                                                  |
|--------------------------------------------|-------------------------------------------------------|
| **主图**                                     |                                                       |
| `image_size`                               | 设置主图尺寸，默认 (300, 220)                                |
| `range_len`                                | 设置随机内容长度范围                                        |
| `range_angle_pos`                          | 设置随机角度范围                                          |
| `range_size`                               | 设置随机内容大小范围                                        |
| `range_colors`                             | 设置随机颜色                                            |
| `display_shadow`                           | 设置是否显示阴影                                          |
| `shadow_color`                             | 设置阴影颜色                                            |
| `shadow_point`                             | 设置阴影偏移位置                                          |
| `image_alpha`                              | 设置主图透明度                                           |
| `use_shape_original_color`                 | 设置是否使用图形原始颜色，"图形点选"有效                       |
| **缩略图**                                    |                                                       |
| `thumb_image_size`                         | 设置缩略尺寸，默认 (150, 40)                              |
| `range_verify_len`                         | 设置校验内容的随机长度范围                                   |
| `disabled_range_verify_len`                | 禁用校验内容的随机长度，与主图内容的长度保持一致                  |
| `range_thumb_size`                         | 设置随机缩略内容随机大小范围                                |
| `range_thumb_colors`                       | 设置缩略随机颜色范围                                      |
| `range_thumb_bg_colors`                    | 设置缩略随机背景颜色范围                                    |
| `is_thumb_non_deform_ability`              | 设置缩略图内容不变形，不受背景影响                             |
| `thumb_bg_distort`                         | 设置缩略图背景扭曲等级 (1-5)                               |
| `thumb_bg_circles_num`                     | 设置缩略图绘制小圆点数量                                    |
| `thumb_bg_slim_line_num`                   | 设置缩略图绘制线条数量                                     |

### 设置资源
> `builder.set_resources(chars=..., fonts=..., backgrounds=..., ...)`

| Options                                   | Desc      |
|-------------------------------------------|-----------|
| `chars`                                   | 设置文本种子    |
| `shapes`                                  | 设置图形种子    |
| `fonts`                                   | 设置字体      |
| `backgrounds`                             | 设置主图背景    |
| `thumb_backgrounds`                       | 设置缩略图背景   |

### 验证码数据
> `capt_data = captcha.generate()`

| Method                                   | Desc      |
|------------------------------------------|-----------|
| `get_data()`                             | 获取当前校验的信息 |
| `get_master_image()`                     | 获取主图      |
| `get_thumb_image()`                      | 获取缩略图     |

### 验证码校验
> `result = click_validate(src_x, src_y, x, y, width, height, padding_value)`

| Params       | Desc               |
|--------------|--------------------|
| `src_x`      | 用户交互的 X 值          |
| `src_y`      | 用户交互的 Y 值          |
| `x`          | 验证码校验的 X 值         |
| `y`          | 验证码校验的 Y 值         |
| `width`      | 验证码校验的 Width 值     |
| `height`     | 验证码校验的 Height 值    |
| `padding_value` | 控制误差值              |

<br/>

### 注意事项

- 字符集（`chars`）或图形集（`shapes`）的长度必须大于 `range_len.max`，否则会触发错误。
- 图形模式需要提供有效的图像资源（`shapes`），否则会触发错误。
- 背景图像不能为空，否则会触发错误。

<br />

## 🖖 滑动/拖拽验证码（Slide/Drag-Drop）

滑动验证码要求用户将拼图块滑动到主图像中的正确位置，支持两种模式：

- **基本模式**：拼图块沿固定 Y 轴滑动，适合简单验证场景。
- **拖拽模式**：拼图块可以在更大范围内自由拖动，适合需要更高交互自由度的场景。

### 工作原理

1. **生成主图像**（`master_image`）：包含拼图块的缺口和阴影效果，通常为 JPEG 格式。
2. **生成拼图图像**（`tile_image`）：用户需要滑动的拼图块，通常为 PNG 格式。
3. **用户交互**：用户滑动拼图块到目标位置（`tile_x`, `tile_y`），前端捕获滑动终点坐标。
4. **验证逻辑**：后端比较用户滑动的位置与目标位置是否匹配。

### 代码示例

```python
from py_captcha import SlideBuilder
from py_captcha.slide.block import GraphImage
from PIL import Image

# 创建构建器
builder = SlideBuilder()

# 加载资源
backgrounds = [Image.open('path/to/bg.jpg')]

# 构建拼图图形
graph_images = []
graph_image = GraphImage()
graph_image.overlay_image = Image.open('path/to/tile.png')
graph_image.shadow_image = Image.open('path/to/tile-shadow.png')
graph_image.mask_image = Image.open('path/to/tile-mask.png')
graph_images.append(graph_image)

# 设置资源
builder.set_resources(
    graph_images=graph_images,
    backgrounds=backgrounds,
)

# 生成验证码
captcha = builder.make()
capt_data = captcha.generate()

# 获取数据
block = capt_data.get_data()
master_image = capt_data.get_master_image()
tile_image = capt_data.get_tile_image()

# 转换为 Base64
master_base64 = master_image.to_base64()
tile_base64 = tile_image.to_base64()

print(f"拼图信息: {block}")
print(f"主图: {master_base64}")
print(f"拼图: {tile_base64}")
```

### 创建实例
- `builder.make()` - 基本模式（固定 Y 轴滑动）
- `builder.make_drag_drop()` - 拖拽模式（范围内自由拖动）

### 配置选项
> `SlideBuilder(option_name=value, ...)` 或 `builder.set_options(option_name=value, ...)`

| Options                                                        | Desc              |
|----------------------------------------------------------------|-------------------|
| `image_size`                                                   | 设置主图尺寸，默认 (300, 220) |
| `image_alpha`                                                  | 设置主图透明度           |
| `range_graph_size`                                             | 设置图形随机尺寸范围        |
| `range_graph_angle_pos`                                        | 设置图形随机角度范围        |
| `gen_graph_number`                                             | 设置图形个数            |
| `enable_graph_vertical_random`                                 | 设置图形水平方向是否随机排序    |
| `range_dead_zone_directions`                                   | 设置贴图盲区            |

### 设置资源
> `builder.set_resources(graph_images=..., backgrounds=..., ...)`

| Options                                       | Desc     |
|-----------------------------------------------|----------|
| `backgrounds`                                 | 设置主图背景   |
| `graph_images`                                | 设置贴图的图形  |

### 验证码数据
> `capt_data = captcha.generate()`

| Method                                   | Desc        |
|------------------------------------------|-------------|
| `get_data()`                             | 获取当前校验的信息   |
| `get_master_image()`                     | 获取主图        |
| `get_tile_image()`                       | 获取缩略图       |

### 验证码校验
> `result = slide_validate(src_x, src_y, x, y, padding_value)`

| Params       | Desc            |
|--------------|-----------------|
| `src_x`      | 用户交互的 X 值       |
| `src_y`      | 用户交互的 Y 值       |
| `x`          | 验证码校验的 X 值      |
| `y`          | 验证码校验的 Y 值      |
| `padding_value` | 控制误差值           |

<br/>

### 注意事项

- 拼图块的图像资源（`overlay_image`, `shadow_image`, `mask_image`）必须有效，否则会触发错误。
- 背景图像不能为空，否则会触发错误。
- 基本模式下，拼图块的 Y 坐标固定；拖拽模式下，Y 坐标可根据 `range_dead_zone_directions` 随机分布。
- 拖拽模式适合需要更高交互自由度的场景，但可能增加用户操作时间。

<br />

## 🖖 旋转验证码（Rotate）

旋转验证码要求用户旋转缩略图使其与主图像的角度对齐，适合需要直观交互的场景。

### 工作原理

1. **生成主图像**（`master_image`）：包含旋转后的背景图像，通常为 PNG 格式。
2. **生成缩略图**（`thumb_image`）：从主图像裁剪并应用圆形裁剪和透明度效果，通常为 PNG 格式。
3. **用户交互**：用户旋转缩略图到目标角度（`block.angle`），前端捕获旋转角度。
4. **验证逻辑**：后端比较用户旋转的角度与目标角度是否匹配。

### 代码示例

```python
from py_captcha import RotateBuilder
from PIL import Image

# 创建构建器
builder = RotateBuilder()

# 加载资源
backgrounds = [
    Image.open('path/to/bg.jpg'),
    Image.open('path/to/bg1.jpg'),
]

# 设置资源
builder.set_resources(
    images=backgrounds,
)

# 生成验证码
captcha = builder.make()
capt_data = captcha.generate()

# 获取数据
block = capt_data.get_data()
master_image = capt_data.get_master_image()
thumb_image = capt_data.get_thumb_image()

# 转换为 Base64
master_base64 = master_image.to_base64()
thumb_base64 = thumb_image.to_base64()

print(f"旋转信息: {block}")
print(f"主图: {master_base64}")
print(f"缩略图: {thumb_base64}")
```

### 创建实例
- `builder.make()` - 旋转模式

### 配置选项
> `RotateBuilder(option_name=value, ...)` 或 `builder.set_options(option_name=value, ...)`

| Options                                          | Desc              |
|--------------------------------------------------|-------------------|
| `image_square_size`                              | 设置主图大小，默认 220x220 |
| `range_angle_pos`                                | 设置校验随机角度范围        |
| `range_thumb_image_square_size`                  | 设置缩略图大小           |
| `thumb_image_alpha`                              | 设置缩略图透明度          |

### 设置资源
> `builder.set_resources(images=..., ...)`

| Options                                    | Desc       |
|--------------------------------------------|------------|
| `images`                                   | 设置主图图片     |

### 验证码数据
> `capt_data = captcha.generate()`

| Method                                   | Desc        |
|------------------------------------------|-------------|
| `get_data()`                             | 获取当前校验的信息   |
| `get_master_image()`                     | 获取主图        |
| `get_thumb_image()`                      | 获取缩略图       |

### 验证码校验
> `result = rotate_validate(src_angle, angle, padding_value)`

| Params       | Desc  |
|--------------|-------|
| `src_angle`  | 用户交互的角度 |
| `angle`      | 验证码校验的角度 |
| `padding_value` | 控制误差值 |

<br/>

### 注意事项

- 背景图像不能为空，否则会触发错误。
- 确保背景图像是有效的 `PIL.Image.Image` 类型，否则会触发错误。
- 缩略图会自动应用圆形裁剪效果，确保背景图像分辨率足够以避免模糊。

<br/>

## 验证码图像

### JPEGImageData

| Method                                    | Desc |
|-------------------------------------------|------|
| `get()`                                   | 获取原图像 |
| `to_bytes()`                              | 转为字节数组 |
| `to_bytes_with_quality(quality)`          | 指定清晰度转为字节数组 |
| `to_base64()`                             | 转为 Base64 字符串，带 "data:image/jpeg;base64," 前缀 |
| `to_base64_data()`                        | 转为 Base64 字符串 |
| `to_base64_with_quality(quality)`         | 指定清晰度转为 Base64 字符串，带 "data:image/jpeg;base64," 前缀 |
| `to_base64_data_with_quality(quality)`    | 指定清晰度转为 Base64 字符串 |
| `save_to_file(filepath, quality)`         | 保存 JPEG 到文件 |

### PNGImageData

| Method                                    | Desc |
|-------------------------------------------|------|
| `get()`                                   | 获取原图像 |
| `to_bytes()`                              | 转为字节数组 |
| `to_base64()`                             | 转为 Base64 字符串，带 "data:image/png;base64," 前缀 |
| `to_base64_data()`                        | 转为 Base64 字符串 |
| `save_to_file(filepath)`                  | 保存到文件 |

<br/>


<br/>

## LICENSE
PyCaptcha source code is licensed under the Apache Licence, Version 2.0 [http://www.apache.org/licenses/LICENSE-2.0.html](http://www.apache.org/licenses/LICENSE-2.0.html)

<br/>

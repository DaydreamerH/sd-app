<template>
	<view class='row'>
		<uv-toast ref='toast'></uv-toast>
		<uv-tabs :list="bigList" :is-scroll="false" @change="change_big" :activeStyle="{
			color: '#FF5A5F',
			fontWeight: 'bold',
			transform: 'scale(1.05)'
		}" lineColor='#FF5A5F'></uv-tabs>
		<view v-if='paint_type==1||paint_type==0'>
			<view>
				<uv-popup ref='popup' bg-color="none">
					<img :src="ImgUrl" class="SeeSeeImg" radius='20rpx' @click='closeImg'>
				</uv-popup>
				<uv-popup ref='title' round="20rpx">
					<text class='GiveTitle'>取个名字吧</text>
					<view>
						<uv-input v-model='title' class='TitleInput' placeholder="字数不超过20字" maxlength="20"></uv-input>
					</view>
					<uv-button @click="PostImg" class='UpButton'>确认发表</uv-button>
				</uv-popup>
				<view class='Card'>
					<view class='img_upload' v-if='paint_type==1'>
						<text class='Res'>选择图像</text>
						<view class='upBox'>
							<uv-upload :maxCount="1" @afterRead="afterRead" width="400rpx" height="300rpx"
								class='upload_image'>
								<uv-image v-if='select_img!=""' :src='select_img' mode='aspectFit' radius="10rpx"
									width='400rpx' height='300rpx'>
								</uv-image>
							</uv-upload>
						</view>
						<view style="display: flex;">
							<uv-button class='clear_button' type='primary' color="#FF5A5F" :disabled="clearAble"
								@click="clear_mask">清除涂抹</uv-button>
							<uv-button class='inpaint_button' type='primary' @click="to_inpaint" color="#FF5A5F"
								:disabled="inpaintAble">局部重绘</uv-button>
						</view>
						<uv-gap height="10rpx" bgColor="#f3f4f6"></uv-gap>
					</view>
					<view class='PrevCard'>
						<text class='Res'>绘制结果</text>
						<br>
						<view class='ImgBox'>
							<uv-image :src='ImgUrl' mode='aspectFit' radius="10rpx" width='400rpx' height='300rpx'
								@click='SeeSee'>
							</uv-image>
						</view>
						<view class='progress_text' v-if="paint_state">
							{{loadText}}
						</view>
						<view class='progress_box' v-if='paint_state'>
							<uv-line-progress :percentage="progress" activeColor="#FF5A5F"></uv-line-progress>
						</view>
						<view style="display: flex;">
							<uv-button class='SaveButton' @click="SaveImg" v-if="!AnyImg" color="#FF5A5F"
								icon="download" iconColor="white" shape="circle"></uv-button>
							<uv-button class='PostButton' type='primary' @click="beforePostImg" :disabled="Post"
								color="#FF5A5F" v-if="!AnyImg">发表作品</uv-button>
							<uv-button class='ShareButton' v-if="!AnyImg" color="#FF5A5F" icon="share" iconColor="white"
								shape="circle"></uv-button>
						</view>

					</view>
					<uv-gap height="10rpx" bgColor="#f3f4f6"></uv-gap>
					<uv-tabs :list="smallList" :is-scroll="false" :current="current" @change="change" :activeStyle="{
						color: '#FF5A5F',
						fontWeight: 'bold',
						transform: 'scale(1.05)'
			    	}" lineColor='#FF5A5F'></uv-tabs>
					<uv-collapse :border="false">
						<uv-collapse-item title='模型介绍'>
							<view style='display: flex;'>
								<uv-image :src='imgPrv[current].url' width='200rpx' height="200rpx"
									radius='10rpx'></uv-image>
								<text>{{txtPrv[current].text}}</text>
							</view>
						</uv-collapse-item>
						<uv-collapse-item title="描述词">
							<view>
								<view class='PromptCard'>
									<view class='label_prompt'>
										<text>正面词</text>
										<uv-button icon='trash' class='trash_button' size="mini" shape="circle"
											color="#f95959" plain iconColor="#f95959" @click="clear_prom"></uv-button>
									</view>
									<view>
										<uv-textarea v-model="form.prompt" placeholder="Prompts in English" class='text'
											maxlength="650" :count="true" height="200rpx"></uv-textarea>
									</view>
								</view>
								<view class='PromptCard'>
									<view class='label_prompt'>
										<text>负面词</text>
										<uv-button icon='trash' class='trash_button' size="mini" shape="circle"
											color="#f95959" plain iconColor="#f95959" @click='clear_n_prom'></uv-button>
									</view>
									<view>
										<uv-textarea v-model="form.negative_prompt"
											placeholder="Negative_prompts in English" class='text' maxlength="650"
											:count="true" height="200rpx"></uv-textarea>
									</view>
								</view>
							</view>
						</uv-collapse-item>
						<uv-collapse-item :title="HWTitle">
							<text class='ps'>宽高最小值100，最大值700</text>
							<view style='display: flex;'>
								<view class='SliderCard'>
									<text class='label'>宽</text>
									<view class='HWInput'>
										<uv-input type="number" class='HWInput' v-model='form.width'></uv-input>
									</view>
								</view>
								<view class='SliderCard'>
									<text class='label'>高</text>
									<view class='HWInput'>
										<uv-input type="number" class='HWInput' v-model='form.height'></uv-input>
									</view>
								</view>
							</view>
						</uv-collapse-item>
						<uv-collapse-item title="采样方法">
							<uv-radio-group v-model="form.sampler_index">
								<uv-radio shape="square" :customStyle="{margin: '8px'}"
									v-for="(item, index) in radiolist" :key="index" :label="item.name"
									:name="item.name">
								</uv-radio>
							</uv-radio-group>
						</uv-collapse-item>
						<uv-collapse-item title="详细参数">
							<view class='MoreCard'>
								<text class="ps">开启面部修复或者丰富细节等将增大绘制时间</text>
								<view style="display: flex;margin-bottom: 30rpx;margin-top: 20rpx;">
									<text class='label'>生成步数</text>
									<view class='InputBox'>
										<uv-input type="number" v-model='form.steps' placeholder="10~50"></uv-input>
									</view>
									<text class='label'>随机数种子</text>
									<view class='InputBox'>
										<uv-input type="number" v-model='form.seed'></uv-input>
									</view>
								</view>
								<view style="display: flex;margin-bottom: 30rpx;margin-top: 20rpx;">
									<text class='label'>词条权重</text>
									<view class='InputBox'>
										<uv-input type="number" v-model='form.cfg_scale' placeholder="1~25"></uv-input>
									</view>
									<view v-if='paint_type==1' style="display: flex;">
										<text class='label'>重绘程度</text>
										<view class='InputBox'>
											<uv-input type="number" v-model='form.denoising_strength'
												placeholder="0.1~0.9"></uv-input>
										</view>
									</view>
								</view>
								<view style="display: flex;flex-wrap:wrap">
									<text style='margin-right: 10rpx;padding-top: 10rpx;'>面部修复</text>
									<uv-switch v-model='form.restore_faces' active-color="#FF5A5F"
										inactive-color="#FFE5F1"></uv-switch>
									<view style="display: flex;" v-if='paint_type==0'>
										<text
											style='margin-right: 10rpx;padding-top: 10rpx;margin-left: 100rpx;'>丰富细节</text>
										<uv-switch v-model='form.enable_hr' active-color="#FF5A5F"
											inactive-color="#FFE5F1"></uv-switch>
									</view>
								</view>
							</view>
						</uv-collapse-item>
					</uv-collapse>
					<uv-button @click="paint" class='button' type='primary' color="#FF5A5F"
						v-if="!PaintState">创作</uv-button>
					<uv-button @click="interrupt" class='button' type='primary' color="#FF5A5F"
						v-if="PaintState">中止</uv-button>
					<br>
				</view>
			</view>
		</view>
		<view v-if='paint_type==2'>
			<uv-collapse :border="false" ref='com'>
				<uv-collapse-item title="通用正面词">
					<view style="display: flex;">
						<view v-for="(word,index) in comment_prompts" :key="index" style="margin-right: 10rpx;">
							<uv-tags :text="word.ch" shape="circle" plain borderColor="#FF5A5F" color="#FF5A5F"
								bgColor="#FFE5F1" @click='add_prompt(word.en,word.ch)'></uv-tags>
						</view>
					</view>
				</uv-collapse-item>
				<uv-collapse-item title='艺术风格正面词'>
					<view style="display: flex;flex-wrap: wrap;">
						<view v-for="(word,index) in style_prompts" :key="index"
							style="margin-right: 10rpx; margin-bottom: 10rpx;">
							<uv-tags :text="word.ch" shape="circle" plain borderColor="#FF5A5F" color="#FF5A5F"
								bgColor="#FFE5F1" @click='add_prompt(word.en,word.ch)'></uv-tags>
						</view>
					</view>
				</uv-collapse-item>
				<uv-collapse-item title='光照效果正面词'>
					<view style="display: flex;flex-wrap: wrap;">
						<view v-for="(word,index) in light_prompts" :key="index"
							style="margin-right: 10rpx; margin-bottom: 10rpx;">
							<uv-tags :text="word.ch" shape="circle" plain borderColor="#FF5A5F" color="#FF5A5F"
								bgColor="#FFE5F1" @click='add_prompt(word.en,word.ch)'></uv-tags>
						</view>
					</view>
				</uv-collapse-item>
			</uv-collapse>
		</view>
		<view v-if='paint_type==3'>
			<uv-collapse :border="false" ref="scene">
				<uv-collapse-item title='自然景观正面词'>
					<view style="display: flex;flex-wrap: wrap;">
						<view v-for="(word,index) in nature_prompts" :key="index"
							style="margin-right: 10rpx; margin-bottom: 10rpx;">
							<uv-tags :text="word.ch" shape="circle" plain borderColor="#FF5A5F" color="#FF5A5F"
								bgColor="#FFE5F1" @click='add_prompt(word.en,word.ch)'></uv-tags>
						</view>
					</view>
				</uv-collapse-item>
				<uv-collapse-item title='室内建筑正面词'>
					<view style="display: flex;flex-wrap: wrap;">
						<view v-for="(word,index) in indoor_prompts" :key="index"
							style="margin-right: 10rpx; margin-bottom: 10rpx;">
							<uv-tags :text="word.ch" shape="circle" plain borderColor="#FF5A5F" color="#FF5A5F"
								bgColor="#FFE5F1" @click='add_prompt(word.en,word.ch)'></uv-tags>
						</view>
					</view>
				</uv-collapse-item>
				<uv-collapse-item title='背景氛围正面词'>
					<view style="display: flex;flex-wrap: wrap;">
						<view v-for="(word,index) in festival_prompts" :key="index"
							style="margin-right: 10rpx; margin-bottom: 10rpx;">
							<uv-tags :text="word.ch" shape="circle" plain borderColor="#FF5A5F" color="#FF5A5F"
								bgColor="#FFE5F1" @click='add_prompt(word.en,word.ch)'></uv-tags>
						</view>
					</view>
				</uv-collapse-item>
			</uv-collapse>
		</view>
		<view v-if='paint_type==4'>
			<uv-collapse :border="false" ref='peo'>
				<uv-collapse-item title='人物身份正面词'>
					<view style="display: flex;flex-wrap: wrap;">
						<view v-for="(word,index) in identity_prompts" :key="index"
							style="margin-right: 10rpx; margin-bottom: 10rpx;">
							<uv-tags :text="word.ch" shape="circle" plain borderColor="#FF5A5F" color="#FF5A5F"
								bgColor="#FFE5F1" @click='add_prompt(word.en,word.ch)'></uv-tags>
						</view>
					</view>
				</uv-collapse-item>
				<uv-collapse-item title='人物特征正面词'>
					<view style="display: flex;flex-wrap: wrap;">
						<view v-for="(word,index) in people_prompts" :key="index"
							style="margin-right: 10rpx; margin-bottom: 10rpx;">
							<uv-tags :text="word.ch" shape="circle" plain borderColor="#FF5A5F" color="#FF5A5F"
								bgColor="#FFE5F1" @click='add_prompt(word.en,word.ch)'></uv-tags>
						</view>
					</view>
				</uv-collapse-item>
				<uv-collapse-item title='人物表情正面词'>
					<view style="display: flex;flex-wrap: wrap;">
						<view v-for="(word,index) in expression_prompts" :key="index"
							style="margin-right: 10rpx; margin-bottom: 10rpx;">
							<uv-tags :text="word.ch" shape="circle" plain borderColor="#FF5A5F" color="#FF5A5F"
								bgColor="#FFE5F1" @click='add_prompt(word.en,word.ch)'></uv-tags>
						</view>
					</view>
				</uv-collapse-item>
				<uv-collapse-item title='人物服饰正面词'>
					<view style="display: flex;flex-wrap: wrap;">
						<view v-for="(word,index) in outlook_prompts" :key="index"
							style="margin-right: 10rpx; margin-bottom: 10rpx;">
							<uv-tags :text="word.ch" shape="circle" plain borderColor="#FF5A5F" color="#FF5A5F"
								bgColor="#FFE5F1" @click='add_prompt(word.en,word.ch)'></uv-tags>
						</view>
					</view>
				</uv-collapse-item>
			</uv-collapse>
		</view>
	</view>
</template>

<script>
	import {
		pathToBase64,
		base64ToPath
	} from 'image-tools'

	export default {
		data() {
			return {
				form: {
					denoising_strength: 0.7,
					prompt: '',
					negative_prompt: '',
					steps: 25,
					width: 512,
					height: 512,
					seed: -1,
					batch_size: 1,
					n_iter: 1,
					cfg_scale: 7,
					restore_faces: true,
					tiling: false,
					override_settings: {
						sd_model_checkpoint: "meinamix_meinaV11.safetensors [54ef3e3610]"
					},
					sampler_index: "DPM++ 2M Karras",
					enable_hr: false,
				},
				smallList: [{
					name: '动漫卡通'
				}, {
					name: '建筑艺术'
				}, {
					name: '写实人像'
				}, {
					name: '欧美漫画'
				}],
				current: 0,
				imgPrv: [{
					url: require('../../static/model_prev/anime.png')
				}, {
					url: require('../../static/model_prev/architecture.png')
				}, {
					url: require('../../static/model_prev/real.png')
				}, {
					url: require('../../static/model_prev/west.png')
				}],
				txtPrv: [{
					text: "该模型的主要画风为日式动漫风格"
				}, {
					text: '该模型主要绘制建筑'
				}, {
					text: '该模型的主要画风为写实风格'
				}, {
					text: '该模型的主要画风为欧美漫画'
				}],
				model_list: [
					"meinamix_meinaV11.safetensors [54ef3e3610]",
					"architectureExterior_v40Exterior.safetensors [03b2d23370]",
					"majicmixRealistic_betterV2V25.safetensors [d7e2ac2f4a]",
					"toonyou_beta6 (1).safetensors [e8d456c42e]"
				],
				paint_state: false,
				ImgUrl: '',
				u_info: {
					uid: '',
					secret: ''
				},
				title: '',
				para: '',
				postAble: false,
				tag: '',
				bigList: [{
						name: "文生图"
					},
					{
						name: "图生图"
					}, {
						name: '通用词条'
					}, {
						name: '场景词条'
					}, {
						name: '人物词条'
					}
				],
				paint_type: 0,
				imgForm: {
					init_images: [],
					resize_mode: 1
				},
				select_img: '',
				in_type: false,
				img_file: '',
				mask: '',
				comment_prompts: [],
				style_prompts: [],
				nature_prompts: [],
				people_prompts: [],
				identity_prompts: [],
				expression_prompts: [],
				outlook_prompts: [],
				light_prompts: [],
				indoor_prompts: [],
				festival_prompts: [],
				radiolist: [{
					name: 'Euler a'
				}, {
					name: 'DPM2'
				}, {
					name: 'DPM++ 2S a'
				}, {
					name: 'DPM++ 2M'
				}, {
					name: 'DPM2 a Karras'
				}, {
					name: 'DPM++ 2M Karras'
				}, {
					name: 'DPM++ SDE Karras'
				}, {
					name: 'DPM fast'
				}],
				timer: '',
				progress: 0,
				timer_life: false,
				paint_url:'http://localhost:7777'
			}
		},
		methods: {
			clear_timer() {
				if (this.timer_life) {
					clearInterval(this.timer)
					this.timer_life = false
				}
				this.progress = 0
			},
			interrupt() {
				const form = {
					task_id: this.u_info.uid
				}
				let _this = this
				uni.request({
					url: _this.paint_url+'/sdapi/v1/interrupt',
					method: 'POST',
					data: form
				}).then(function(resp) {
					if (resp.data == 'success') {
						_this.clear_timer()
					}
				})
			},
			add_prompt(en, ch) {
				if (this.form.prompt != '')
					this.form.prompt += ', ' + en
				else this.form.prompt = en
				this.$refs.toast.show({
					message: ch + ' 添加成功',
					type: 'success',
					position: 'top',
					duration:'600'
				})
			},
			clear_mask() {
				this.mask = ''
			},
			to_inpaint() {
				uni.setStorageSync('img_file', this.img_file)
				uni.navigateTo({
					url: '/pages/inpaint/inpaint'
				})
			},
			basic_check() {
				if (this.form.width < 100) {
					this.$refs.toast.show({
						message: '宽度不得小于100',
						type: 'error',
						position: 'top'
					})
					return false
				} else if (this.form.width > 700) {
					this.$refs.toast.show({
						message: '宽度不得大于700',
						type: 'error',
						position: 'top'
					})
					return false
				} else if (this.form.height < 100) {
					this.$refs.toast.show({
						message: '高度不得小于100',
						type: 'error',
						position: 'top'
					})
					return false
				} else if (this.form.height > 700) {
					this.$refs.toast.show({
						message: '高度不得大于700',
						type: 'error',
						position: 'top'
					})
					return false
				} else if (this.form.steps < 10 || this.form.steps > 50) {
					this.$refs.toast.show({
						message: '步数设置错误',
						type: 'error',
						position: 'top'
					})
					return false
				} else if (this.form.cfg_scale < 1 || this.form.cfg_scale > 25) {
					this.$refs.toast.show({
						message: '词条权重错误',
						type: 'error',
						position: 'top'
					})
					return false
				} else if (this.u_info.uid == "" || this.u_info.secret == "") {
					this.$refs.toast.show({
						message: '请先登录',
						type: 'error',
						position: 'top'
					})
					return false
				}
				return true
			},
			change_big(item) {
				if (this.ImgUrl != "" && this.paint_type == 0) {
					this.select_img = this.ImgUrl
					this.imgForm.init_images[0] = this.ImgUrl
					this.img_file = this.ImgUrl
				}
				if (item.index >= 2)
					this.$nextTick(() => {
						if (item.index == 2) this.$refs.com.init()
						else if (item.index == 3) this.$refs.scene.init()
						else if (item.index == 4) this.$refs.peo.init()
					})
				if (this.form.denoising_strength == 0 && item.index == 1) this.form.denoising_strength = 0.5
				this.paint_type = item.index

			},
			paint() {
				if (this.paint_type == 0)
					this.txt_img()
				else this.img_img()
			},
			txt_img() {
				if (!this.basic_check()) {
					return false
				}
				let _this = this
				this.paint_state = true
				if (this.form.enable_hr) {
					this.form.denoising_strength = 0.7
					this.form['hr_upscaler'] = 'R-ESRGAN 4x+ Anime6B'
				} else this.form.denoising_strength = 0
				this.form['uid'] = this.u_info.uid
				this.form['secret'] = this.u_info.secret
				uni.request({
					url: _this.paint_url+"/sdapi/v1/txt2img",
					method: 'POST',
					data: _this.form
				}).then(function(resp) {
					_this.paint_state = false
					_this.ImgUrl = 'data:image/jpg;base64,' + resp.data.images[0]
					_this.select_img = _this.ImgUrl
					_this.para = resp.data.parameters
					_this.postAble = true
					_this.tag = _this.smallList[_this.current].name
					_this.clear_timer()
				}).catch(e => {
					_this.$refs.toast.show({
						message: '服务器罢工了qwq',
						type: 'error'
					})
					_this.clear_timer()
					_this.paint_state = false
				})
				setTimeout(() => {
					this.progress_timer()
				}, 1000)
			},
			img_img() {
				if (!this.basic_check()) return false
				if (this.imgForm.init_images.length == 0) {
					this.$refs.toast.show({
						message: '请先上传图像',
						type: 'error',
						position: 'top'
					})
					return false
				} else if (this.form.denoising_strength < 0.1 || this.form.denoising_strength > 0.9) {
					this.$refs.toast.show({
						message: '重绘程度设置错误',
						type: 'error',
						position: 'top'
					})
					return false
				}
				let _this = this
				this.paint_state = true
				Object.assign(this.imgForm, this.form)
				this.imgForm['uid'] = this.u_info.uid
				this.imgForm['secret'] = this.u_info.secret
				let form = Object.assign({}, this.imgForm)
				if (this.mask != '') {
					form['mask'] = this.mask
				}
				uni.request({
					url: _this.paint_url+"/sdapi/v1/img2img",
					method: 'POST',
					data: form
				}).then(function(resp) {
					_this.paint_state = false
					_this.ImgUrl = 'data:image/jpg;base64,' + resp.data.images[0]
					_this.para = resp.data.parameters
					_this.postAble = true
					_this.tag = _this.smallList[_this.current].name
					_this.clear_timer()
				}).catch(e => {
					console.log(e)
					_this.$refs.toast.show({
						message: '服务器罢工了qwq',
						type: 'error'
					})
					_this.clear_timer()
					_this.paint_state = false
				})
				setTimeout(() => {
					this.progress_timer()
				}, 1000)
			},
			progress_timer() {
				this.timer = setInterval(() => {
					this.get_progress()
				}, 700)
				this.timer_life = true
			},
			get_progress() {
				const form = {
					task_id: this.u_info.uid
				}
				let _this = this
				uni.request({
					url: _this.paint_url+'/sdapi/v1/progress',
					method: 'POST',
					data: form
				}).then(function(resp) {
					if (resp.data.progress) {
						_this.progress = resp.data.progress * 100
						_this.progress = ~~_this.progress
					} else _this.progress = 0
				})
			},
			change(index) {
				this.current = index.index
				this.form.override_settings.sd_model_checkpoint = this.model_list[this.current]
			},
			SeeSee() {
				if (this.ImgUrl != '')
					this.$refs.popup.open()
			},
			SaveImg() {
				let base64 = this.ImgUrl
				const bitmap = new plus.nativeObj.Bitmap("test");
				let _this = this
				bitmap.loadBase64Data(base64, function() {
					const url = "_doc/" + new Date().getTime() + ".png"; // url为时间戳命名方式
					bitmap.save(url, {
						overwrite: true, // 是否覆盖
						// quality: 'quality'  // 图片清晰度
					}, (i) => {
						uni.saveImageToPhotosAlbum({
							filePath: url,
							success: function() {
								_this.$refs.toast.show({
									message: '图片保存成功',
									type: 'success',
									position: 'top'
								})
								bitmap.clear()
							}
						});
					}, (e) => {
						_this.$refs.toast.show({
							message: '图片保存失败',
							type: 'error',
							position: 'top'
						})
						bitmap.clear()
					});
				}, (e) => {
					_this.$refs.toast.show({
						message: '图片保存失败',
						type: 'error',
						position: 'top'
					})
					bitmap.clear()
				});
			},
			PostImg() {
				let base64 = this.ImgUrl
				const bitmap = new plus.nativeObj.Bitmap("test")
				let _this = this
				this.postAble = false
				if (this.title.length == 0) {
					this.$refs.toast.show({
						message: "请输入标题",
						type: 'error'
					})
					this.postAble = true
					return
				}
				bitmap.loadBase64Data(base64, function() {
					const url = "_doc/" + new Date().getTime() + ".png"; // url为时间戳命名方式
					bitmap.save(url, {
						overwrite: true,
					}, (i) => {
						const form = {
							uid: _this.u_info.uid,
							secret: _this.u_info.secret,
							title: _this.title,
							tag: _this.tag,
							prompt: _this.para.prompt,
							n_prompt: _this.para.negative_prompt
						}
						uni.uploadFile({
							url: 'http://8.137.96.56:3689/img/upload',
							filePath: url,
							name: 'work',
							formData: form
						}).then(function(resp) {
							if (resp.data == 'success') {
								_this.$refs.toast.show({
									message: '发表成功',
									type: 'success',
									position: 'top'
								})
							}
							bitmap.clear()
						}).catch(e => {
							_this.$refs.toast.show({
								message: '服务器出错，发表失败',
								type: 'error',
								position: 'top'
							})
							_this.postAble = true
						})
					}, (e) => {
						_this.$refs.toast.show({
							message: '发表失败',
							type: 'error',
							position: 'top'
						})
						_this.postAble = true
						bitmap.clear()
					});
				}, (e) => {
					_this.$refs.toast.show({
						message: '发表失败',
						type: 'error',
						position: 'top'
					})
					bitmap.clear()
					_this.postAble = false
				})
				_this.$refs.title.close()
			},
			beforePostImg() {
				this.$refs.title.open()
			},
			async afterRead(event) {
				pathToBase64(event.file.url).then(base64 => {
					this.select_img = base64
					this.imgForm.init_images[0] = base64
					this.mask == ''
					this.img_file = base64
				}).catch(e => {
					console.log(e)
				})
			},
			closeImg() {
				this.$refs.popup.close()
			},
			clear_prom() {
				this.form.prompt = ''
			},
			clear_n_prom() {
				this.form.negative_prompt = ''
			}
		},
		computed: {
			HWTitle() {
				return '宽高（' + this.form.width + ',' + this.form.height + ')';
			},
			STitle() {
				return '生成步数 ' + this.form.steps + '步'
			},
			AnyImg() {
				return (this.ImgUrl == '' || this.paint_state)
			},
			Post() {
				return !this.postAble
			},
			clearAble() {
				return this.mask == ''
			},
			inpaintAble() {
				return this.imgForm.init_images[0] == '' || this.select_img == ''
			},
			loadText() {
				if (this.progress <= 0.05) {
					return '排队等待中'
				} else if (this.progress == 100) return '正在抄送'
				else return '努力绘制中'
			},
			PaintState() {
				return this.paint_state
			}
		},
		onShow() {
			let _this = this
			if(uni.getStorageSync('u_info'))
				this.u_info = uni.getStorageSync('u_info')
			else{
				uni.navigateTo({
					url: '/pages/Login/Login'
				})
			}
			if (uni.getStorageInfoSync('mask')) {
				this.mask = uni.getStorageSync('mask')
				uni.removeStorageSync('mask')
			}
		},
		onLoad(option) {
			if (option.prompt) {
				this.form.prompt = option.prompt
				this.form.negative_prompt = option.n_prompt
			}
		},
		mounted() {
			this.comment_prompts = require('../../static/prompts/comment.json')
			this.style_prompts = require('../../static/prompts/style.json')
			this.nature_prompts = require('../../static/prompts/nature.json')
			this.people_prompts = require('../../static/prompts/people.json')
			this.identity_prompts = require('../../static/prompts/identity.json')
			this.expression_prompts = require('../../static/prompts/expression.json')
			this.outlook_prompts = require('../../static/prompts/clothes.json')
			this.light_prompts = require('../../static/prompts/light.json')
			this.indoor_prompts = require('../../static/prompts/indoor.json')
			this.festival_prompts = require('../../static/prompts/festival.json')
		}
	}
</script>

<style lang='scss' scoped>
	.SeeSeeImg {
		width: 750rpx;
		height: auto;
	}

	.row {
		width: 750rpx;
		height: 100vh;

		.status_bar {
			height: var(--status-bar-height);
			width: 100%;
		}

		.Card {
			width: 750rpx;
			height: 100vh;
			background-color: white;
			opacity: 0.92;
			margin-top: 10rpx;

			.img_upload {
				width: 750rpx;
				height: auto;

				.upload_image {
					width: 400rpx;
					margin-left: 175rpx;
				}

				.Res {
					margin-left: 20rpx;
					color: #606266;
				}

				.upBox {
					display: flex;
					margin-bottom: 20rpx;
				}

				.clear_button {
					width: 200rpx;
					margin-bottom: 20rpx;
					margin-left: 150rpx;
					margin-right: 50rpx;
				}

				.inpaint_button {
					width: 200rpx;
				}
			}

			.PrevCard {
				width: 750rpx;
				padding-top: 10rpx;

				.progress_text {
					text-align: center;
					color: #FF5A5F;
					margin-bottom: 10rpx;
					font-size: 30rpx;
				}

				.progress_box {
					width: 400rpx;
					margin-left: 175rpx;
					margin-bottom: 30rpx;
					display: flex;
				}

				.Res {
					margin-left: 20rpx;
					color: #606266;
				}

				.ImgBox {
					width: 400rpx;
					margin-left: 175rpx;
					margin-bottom: 30rpx;
				}

				.SaveButton {
					width: 100rpx;
					margin-left: 130rpx;
					margin-right: 50rpx;
					margin-bottom: 20rpx;
				}

				.PostButton {
					width: 200rpx;
					margin-right: 50rpx;
				}

				.ShareButton {
					width: 100rpx;
				}
			}

			.PromptCard {

				width: 750rpx;
				height: auto;

				.label {
					font-weight: 100;
					margin-top: 10rpx;
				}

				.text {
					width: 650rpx;
					margin-top: 10rpx;
					margin-bottom: 10rpx;

				}
			}

			.ps {
				font-style: italic;
				color: gray;
			}

			.SliderCard {
				height: 90rpx;
				display: flex;
				margin-right: 150rpx;
				margin-top: 20rpx;

				.label {
					font-weight: 100;
					margin-right: 20rpx;
				}

				.HWInput {
					width: 150rpx;

				}
			}

			.MoreCard {
				width: 750rpx;
				height: auto;

				.InputBox {
					width: 150rpx;
					margin-left: 10rpx;
					margin-right: 50rpx;
				}
			}

			.button {
				width: 200rpx;
				margin-left: 275rpx;
				margin-bottom: 50rpx;
				margin-top: 50rpx;
			}
		}

		.inpaint_image {
			width: 750rpx;
			height: auto;

		}

		.canvas {
			width: 750rpx;

		}
	}

	.Image {
		width: 700rpx;
		height: auto;
		margin-left: 25rpx;
	}

	.GiveTitle {
		margin: 20rpx;
		font-size: larger;
	}

	.TitleInput {
		width: 600rpx;
		margin: 40rpx;
	}

	.UpButton {
		width: 200rpx;
		margin-left: 240rpx;
		margin-bottom: 20rpx;
	}

	.label_prompt {
		font-weight: 100;
		margin-top: 10rpx;
		display: flex;

		.trash_button {
			width: 5rpx;
			margin-left: 10rpx;
			padding-bottom: 12rpx;
		}
	}
</style>
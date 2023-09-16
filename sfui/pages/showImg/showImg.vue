<template>
	<view class='row'>
		<uv-modal
			ref="modal"
			content="确认删除图片吗"
			showCancelButton
			@confirm="DelImg"
			@cancel="cancel"
			confirmColor="#FF5A5F"
		></uv-modal>
		<view class='ImageBox'>
			<uv-image :src="info.source" width="750rpx" height="750rpx" mode="aspectFit"></uv-image>
		</view>
		<text class='Title'>
			{{info.title}}
		</text>
		<view class='WriterInfo'>
			<uv-avatar :src='info.painter_avatar' size='40' class='painter_avatar'></uv-avatar>
			<view class='PainterInfo'>
				<view class='painter_name'>{{info.painter_uname}}</view>
				<view class='painter_sign'>{{info.painter_sign}}</view>
			</view>
			<view class='up_info' @click="toOtherSpace" v-if='u_info.uid!=info.painter_uid'>
				进入ta的空间
			</view>
		</view>
		<view class='Main'>
			<view v-if='info.prompt!=""'>
				<view class='Words'>
					<view class='PartText'>正面词</view>
					<view class='Text'>{{info.prompt}}</view>
				</view>
			</view>
			<view v-if='info.n_prompt!=""'>
				<view class='Words'>
					<view class='PartText'>负面词</view>
					<view class='Text'>{{info.n_prompt}}</view>
				</view>
			</view>
			<view class='Words'>
				<view class='PartText'>所用模型:&ensp;{{info.tag}}</view>
			</view>
			<view class='time'>
				{{info.img_time}}
			</view>
			<view class='time'>
				{{info.like_num}}人赞了
			</view>
			<view style='display: flex;'>
				<uv-button icon='star-fill' shape='circle' class='StarButton' @click="like" color="#FF5A5F"
					iconColor="white" v-if='!this.info.like_state'></uv-button>
				<uv-button icon='star-fill' shape='circle' class='StarButton' @click="like" color="#FF5A5F"
					iconColor="#F9D423" v-if='this.info.like_state'></uv-button>
				<uv-button icon='download' shape='circle' class='DownButton' type='primary' @click="download"
					color="#FF5A5F" iconColor="white"></uv-button>
			</view>
		</view>
		<uv-gap height="10rpx" bgColor="#f3f4f6"></uv-gap>
		<uv-button class='PaintButton' icon="photo" @click="toPaint" color="#FFC0CB" iconColor="#FF5A5F"></uv-button>
		<uv-button class='DelButton' icon="trash" @click="preDelImg"
		 color="#FFC0CB" iconColor="#FF5A5F" v-if='info.user_uid==u_info.uid'></uv-button>
		<view class='comment_area'>
			<view class='comTitle'>最新评论</view>
			<uv-collapse :border="false" @open='open_comment' @close='close_comment' ref='coms'>
				<view v-for='(comment,index) in info.com_list' :key='index'>
					<uv-collapse-item :name='comment.cid'>
						<Comment slot="title" :comment="comment" v-if='show_time'></Comment>
						<view v-for='(reply_comment,index) in comment.reply_list' :key='index'>
							<SmallComment :comment='reply_comment'></SmallComment>
						</view>
						<view v-if='!comment.reply_list' style="text-align: center;">暂无回复</view>
					</uv-collapse-item>
					<uv-line></uv-line>
				</view>
			</uv-collapse>
			<uv-load-more :status="loadAble"></uv-load-more>
		</view>

		<view class='comment_input_box' v-if='comment_cid==0'>
			<uv-input maxlength="20" placeholder="请输入评论" class='input_box' v-model="comment_text"></uv-input>
			<uv-button class='comment_button' color="#FF5A5F" shape='circle' @click='PostComment'>评论</uv-button>
		</view>
		<view class='comment_input_box' v-if='comment_cid!=0'>
			<uv-input maxlength="20" placeholder="请回复评论" class='input_box' v-model="comment_text"></uv-input>
			<uv-button class='comment_button' color="#FF5A5F" shape='circle' @click='PostComment'>回复</uv-button>
			<view class='give_up' @click="close_comment">放弃回复</view>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				info: "",
				params: {
					width: "750rpx",
					height: "800rpx",
					blur: "xs",
					image: ''
				},
				u_info: {
					uid: '',
					secret: ''
				},
				iid: '',
				comment_text: '',
				page: 1,
				per_page: 4,
				show_time: false,
				loadAble: 'loadmore',
				comment_cid: 0
			}
		},
		methods: {
			preDelImg(){
				this.$refs.modal.open()
			},
			DelImg(){
				const form = {
					uid:this.u_info.uid,
					secret:this.u_info.secret,
					iid:this.iid
				}
				uni.request({
					url:'http://localhost:3689/img/delete',
					method:'POST',
					data:form
				}).then(function(resp){
					if(resp.data=='success'){
						uni.reLaunch({
							url:'/pages/Square/Square'
						})
					}
				})
			},
			cancel(){
				this.$refs.modal.close()
			},
			open_comment(comment_cid) {
				this.comment_cid = comment_cid
			},
			close_comment() {
				this.comment_cid = 0
			},
			commentSelect() {
				let _this = this
				const form = {
					iid: _this.iid,
					page: _this.page,
					per_page: _this.per_page,
				}
				if (this.page == 1) this.show_time = false
				else form['cid'] = this.info.com_list[0].cid
				uni.request({
					url: "http://localhost:3689/comment/select",
					method: 'POST',
					data: form
				}).then(function(resp) {
					if (_this.page == 1) {
						_this.info.com_list = resp.data.com_list
						_this.show_time = true
					} else _this.info.com_list = _this.info.com_list.concat(resp.data.com_list)
					_this.info.total_compage = resp.data.total_pages
				}).catch(e => {
					console.log(e)
					_this.page -= 1
				})
			},
			like() {
				let _this = this
				const form = {
					uid: _this.u_info.uid,
					secret: _this.u_info.secret,
					iid: this.iid
				}
				if (!this.info.like_state) {
					uni.request({
						url: "http://localhost:3689/like/insert",
						data: form,
						method: "POST"
					}).then(function(resp) {
						if (resp.data == 'success') {
							_this.info.like_state = 1
							_this.info.like_num += 1
						}
					})
				} else {
					uni.request({
						url: "http://localhost:3689/like/delete",
						data: form,
						method: "POST"
					}).then(function(resp) {
						if (resp.data == 'success') {
							_this.info.like_state = 0
							_this.info.like_num -= 1
						} else {
							console.log(resp.data)
						}
					})
				}
			},
			download() {
				let _this = this
				uni.downloadFile({
					url: _this.info.source, // 图像的网络地址
					success: function(res) {
						if (res.statusCode === 200) {
							uni.saveImageToPhotosAlbum({
								filePath: res.tempFilePath,
								success: function() {
									uni.showToast({
										title: '保存成功',
										icon: 'success'
									});
								},
								fail: function(error) {
									uni.showToast({
										title: '保存失败',
										icon: 'none'
									});
									console.log(error);
								}
							});
						} else {
							console.log('下载失败');
						}
					},
					fail: function(error) {
						console.log('下载失败');
						console.log(error);
					}
				});
			},
			PostComment() {
				if (this.comment_text == '') {
					uni.showToast({
						title: '评论不得为空',
						icon: 'error'
					})
					return false
				} else if (this.comment_text.length > 20) {
					uni.showToast({
						title: '评论在20字以内',
						icon: 'error'
					})
					return false
				}
				let form = {}
				if (this.comment_cid == 0)
					form = {
						iid: this.iid,
						uid: this.u_info.uid,
						secret: this.u_info.secret,
						text: this.comment_text
					}
				else form = {
					iid: this.iid,
					uid: this.u_info.uid,
					secret: this.u_info.secret,
					text: this.comment_text,
					pcid: this.comment_cid
				}
				let _this = this
				uni.request({
					url: 'http://localhost:3689/comment/insert',
					method: 'POST',
					data: form
				}).then(function(resp) {
					if (_this.comment_cid == 0)
						_this.info.com_list.unshift(resp.data)
					else {
						for (let i = 0; i < _this.info.com_list.length; i++) {
							if (_this.info.com_list[i].cid == resp.data.pcid) {
								_this.$refs.coms.init()
								if (!_this.info.com_list[i].reply_list) {
									_this.info.com_list[i]["reply_list"] = []
								}
								_this.info.com_list[i].reply_list.unshift(resp.data)
								break
							}
						}
					}
					uni.showToast({
						title: '发表成功'
					})
					_this.comment_cid = 0
					_this.comment_text = ''
				})
			},
			toPaint() {
				uni.reLaunch({
					url: '/pages/Paint/Paint?prompt=' + this.info.prompt + '&n_prompt=' + this.info.n_prompt
				})
			},
			toOtherSpace() {
				let _this = this
				uni.navigateTo({
					url: '/pages/OtherSpace/OtherSpace?uid=' + _this.info.painter_uid,
					fail(e) {
						console.log(e)
					}
				})
			}
		},
		onLoad(option) {
			let _this = this
			const iid = option.iid
			this.iid = iid
			this.u_info.uid = uni.getStorageSync('u_info').uid
			this.u_info.secret = uni.getStorageSync('u_info').secret
			if (this.u_info.uid != '') {
				const form = {
					uid: _this.u_info.uid,
					iid: iid,
					per_page: _this.per_page
				}
				uni.request({
					url: "http://localhost:3689/img/show",
					method: "POST",
					data: form
				}).then(function(resp) {
						if (resp.data != "error") {
							_this.info = resp.data
							if (_this.info.com_list == []) {
								_this.loadAble = 'nomore'
							}
							_this.params.image = _this.info.source
							if (resp.data.com_list != []) _this.show_time = true
						} else {
							uni.showToast({
								icon: None,
								title: "查询失败"
							})
						}
					})
				}
			},
			onReachBottom() {
					this.page += 1
					if (this.page > this.info.total_compage) {
						this.loadAble = 'nomore'
						this.page -= 1
					} else {
						this.loadAble = 'loading'
						this.commentSelect()
						this.loadAble = 'loadmore'
					}
				},

		}
</script>

<style lang='scss' scoped>
	.row {
		width: 750rpx;
		min-height: 100vh;
		height: auto;
		overflow-x: hidden;

		.ImageBox {
			width: 750rpx;
			height: 750rpx;
			background-color: #F2F2F2;
			margin-bottom: 20rpx;
		}

		.Title {
			font-size: 50rpx;
			margin-left: 20rpx;
			font-weight: 350;
		}

		.WriterInfo {
			width: 750rpx;
			height: 130rpx;
			display: flex;
			margin-top: 20rpx;
			margin-left: 10rpx;

			.up_info {
				height: 30rpx;
				text-align: center;
				margin-top: 25rpx;
				margin-left: 140rpx;
				font-size: 30rpx;
				background-color: #FF5A5F;
				color: white;
				border: solid 10rpx #FF5A5F;
				border-radius: 20rpx;
				padding-bottom: 10rpx;
			}

			.PainterInfo {
				display: block;
				width: 300rpx;
				height: auto;

				.painter_name {
					font-weight: 350;
					margin-left: 10rpx;
					margin-top: 15rpx;
					font-size: 30rpx;
				}

				.painter_sign {
					margin-left: 10rpx;
					font-size: 25rpx;
					margin-top: 10rpx;
				}
			}

			.painter_avatar {
				margin-top: 10rpx;
			}
		}

		.Main {
			margin-top: 20rpx;
			width: 750rpx;
			height: auto;
			margin-bottom: 20rpx;

			.Words {
				box-shadow: 0 5rpx 5rpx rgba(0, 0, 0, 0.1);

				.PartText {
					font-size: 40rpx;
					margin-bottom: 10rpx;
				}

				.Text {
					background-color: #F08080;
					margin: 10rpx;
					padding: 20rpx;
					border-radius: 10rpx;
				}

				margin-top: 20rpx;
				width: 700rpx;
				height: auto;
				margin-left: 20rpx;
				padding-left: 10rpx;
				padding-right: 10rpx;
				padding-top: 20rpx;
				padding-bottom: 20rpx;
				margin-bottom: 20rpx;
				background-color: #FF5A5F;
				color:white;
			}

			.tag {
				margin-left: 25rpx;
				margin-bottom: 20rpx;
				margin-top: 20rpx;
				color: #008080;
			}

			.time {
				text-align: center;
				color: darkgray;
				margin-top: 10rpx;
				font-size: 25rpx;
			}

			.StarButton {
				width: 100rpx;
				margin-left: 250rpx;
				margin-top: 20rpx;
				margin-bottom: 10rpx;
			}

			.DownButton {
				width: 100rpx;
				margin-left: 30rpx;
				margin-top: 20rpx;
				margin-bottom: 10rpx;
			}
		}

		.CommentButton {
			bottom: 30rpx;
			right: 30rpx;
			position: fixed;
			width: 100rpx;
			box-shadow: 0 5rpx 5rpx rgba(0, 0, 0, 0.1);
			border-radius: 30rpx;
		}
		.DelButton{
			bottom: 260rpx;
			right: 30rpx;
			position: fixed;
			width: 100rpx;
			box-shadow: 0 5rpx 5rpx rgba(0, 0, 0, 0.1);
			border-radius: 30rpx;
		}
		.PaintButton {
			bottom: 140rpx;
			right: 30rpx;
			position: fixed;
			width: 100rpx;
			box-shadow: 0 5rpx 5rpx rgba(0, 0, 0, 0.1);
			border-radius: 30rpx;
		}

		.GiveTitle {
			margin: 20rpx;
			font-size: larger;
			font-weight: bold;
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

		.comTitle {
			margin-top: 8rpx;
			margin-left: 10rpx;
			margin-bottom: 10rpx;
		}

		.comment_input_box {
			height: 100rpx;
			width: 750rpx;
			position: fixed;
			bottom: 0;
			display: flex;
			background-color: white;

			.comment_button {
				width: 150rpx;
				margin-right: 10rpx;
				height: 80rpx;
				margin-top: 10rpx;
			}

			.input_box {
				width: 530rpx;
				margin-left: 40rpx;
				margin-right: 20rpx;
				height: 60rpx;
				margin-top: 10rpx;
				border-radius: 40rpx;

			}
		}

		.comment_input_box {
			height: 100rpx;
			width: 750rpx;
			position: fixed;
			bottom: 0;
			display: flex;
			background-color: white;

			.comment_button {
				width: auto;
				margin-right: 10rpx;
				height: 80rpx;
				margin-top: 10rpx;
			}

			.input_box {
				width: 450rpx;
				margin-left: 40rpx;
				margin-right: 20rpx;
				height: 60rpx;
				margin-top: 10rpx;
				border-radius: 40rpx;
			}

			.give_up {
				width: 150rpx;
				font-size: 30rpx;
				text-align: center;
				margin-top: 30rpx;
				color: #FF5A5F;
			}
		}

		.comment_area {
			margin-bottom: 100rpx;
		}
	}
</style>
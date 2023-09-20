<template>
	<view class="row">
		<view class="status_bar" style="height: var(--status-bar-height); width: 100%;">
		</view>
		<view class='UserInfo'>
			<view style="display: flex;">
				<uv-avatar :src='u_info.avatar' shape='circle' size='60' class='u_avatar'></uv-avatar>
				<view v-if="u_info.uid!=''" style="display: flex;">
					<view class='u_text_info'>
						<view class='u_name'>{{u_info.uname}}</view>
						<view class='u_sign'>{{u_info.sign}}</view>
					</view>
				</view>
			</view>
			<view class='data_c'>
				<text class='data'>
					<text class='num'>{{work_num}}</text>
					<text style="color: darkgrey;">作品</text>
				</text>
				<text class='data'>
					<text class='num'>{{like_num}}</text>
					<text style="color: darkgrey;">收藏</text>
				</text>
				<text class='data'>
					<text class='num'>{{be_liked_num}}</text>
					<text style="color: darkgrey;">被收藏</text>
				</text>
			</view>
		</view>
		<uv-gap height="10rpx" bgColor="#f3f4f6"></uv-gap>
		<view class='ach_card'>
			<uv-tabs :list="List" :is-scroll="false" @change="change" :activeStyle="{
						color: '#FF5A5F',
						fontWeight: 'bold',
						transform: 'scale(1.05)'
			    	}" lineColor='#FF5A5F' :itemStyle="{
						height:'80rpx'
					}" :current='current'></uv-tabs>
			<uv-loading-icon mode="circle" color="#FF5A5F" class='loading' size='30'
				:show='load_state'></uv-loading-icon>
			<scroll-view scroll-y class='scroll_wrapper' @scrolltolower='getmore()' v-if='total_pages!=0'>
				<view v-for='(imgs,index) in pairedPrevImgs' :key='index' class="ImgsBox">
					<view v-for='(img,index) in imgs' :key='img.iid'>
						<view v-if='show_time&&index==0' @click="toShow(img.iid)">
							<ImgCard v-if='show_time&&index==0' :img_url='img.source' :title='img.title'></ImgCard>
						</view>
						<view v-if='show_time&&index==1' @click="toShow(img.iid)">
							<ImgCardRight v-if='show_time&&index==1' :img_url='img.source' :title='img.title'>
							</ImgCardRight>
						</view>
					</view>
				</view>
				<uv-load-more :status="loadAble"></uv-load-more>
			</scroll-view>
			<uv-empty mode="list" width="300" marginTop="100" iconColor="#F8D9E9" iconSize='130' text='暂无作品'
				textColor="#F8D9E9" textSize="20" v-if='total_pages==0 && load_state==false'></uv-empty>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				u_info: {
					uid: "",
					uname: "",
					sign: "",
					avatar: "",
					secret: ""
				},
				List: [{
					name: 'ta的作品'
				}, {
					name: 'ta的收藏'
				}],
				get_type: 'own',
				my_list: [],
				per_page: 6,
				page: 1,
				total_pages: '',
				show_time: false,
				max_iid: '',
				loadAble: 'loadmore',
				current: 0,
				first: true,
				work_num: 0,
				like_num: 0,
				be_liked_num: 0,
				load_state: true
			};
		},
		methods: {
			change(item) {
				if (item.index == 0) {
					this.get_type = 'own'
					this.page = 1
					this.load_state = true
					this.getImg()
					this.load_state = false
				} else {
					this.get_type = 'like'
					this.page = 1
					this.load_state = true
					this.getImg()
					this.load_state = false
				}
			},
			toShow(iid) {
				uni.navigateTo({
					url: '/pages/showImg/showImg?iid=' + iid
				})
			},
			getmore() {
				this.page += 1
				if (this.page > this.total_pages) {
					this.page -= 1
					this.loadAble = 'nomore'
				} else {
					this.loadAble = 'loading'
					this.getImg()
					this.loadAble = 'loadmore'
				}
			},
			getImg() {
				let form = {}
				if (this.page == 1) {
					this.show_time = false
					form = {
						uid: this.u_info.uid,
						page: 1,
						per_page: this.per_page,
						get_type: this.get_type
					}
				} else {
					form = {
						uid: this.u_info.uid,
						page: this.page,
						per_page: this.per_page,
						get_type: this.get_type,
						max_iid: this.max_iid
					}
				}
				let _this = this
				uni.request({
					url: "http://8.137.96.56:3689/img/select_my",
					method: "POST",
					data: form
				}).then(function(resp) {
					if (_this.page == 1) {
						_this.my_list = resp.data.my_list
						_this.show_time = true
					} else {
						_this.my_list = _this.my_list.concat(resp.data.my_list)
					}
					_this.total_pages = resp.data.total_pages
					if (_this.total_pages <= 1) {
						_this.loadAble = 'nomore'
					}
				})
			}
		},
		onLoad(option) {
			this.u_info.uid = option.uid
			let _this = this
			const form = {
				uid: _this.u_info.uid,
				per_page: _this.per_page
			}
			uni.request({
				url: "http://8.137.96.56:3689/user/getInfo",
				data: form,
				method: 'POST'
			}).then(function(resp) {
				_this.u_info.uname = resp.data.u_info.uname
				_this.u_info.avatar = resp.data.u_info.avatar
				_this.u_info.sign = resp.data.u_info.sign
				_this.total_pages = resp.data.total_pages
				_this.my_list = resp.data.my_list
				_this.show_time = true
				_this.max_iid = resp.data.max_iid
				_this.first = false
				_this.like_num = resp.data.like_num
				_this.be_liked_num = resp.data.be_liked_num
				_this.work_num = resp.data.work_num
				if (_this.total_pages <= 1) {
					_this.loadAble = 'nomore'
				}
				_this.load_state = false
			})
		},
		computed: {
			isLeft(index) {
				if (index % 2 != 0) return false
				return true
			},
			pairedPrevImgs() {
				const pairedPrevImgs = [];
				for (let i = 0; i < this.my_list.length; i += 2) {
					const pair = this.my_list.slice(i, i + 2);
					pairedPrevImgs.push(pair);
				}
				return pairedPrevImgs;
			}
		}
	}
</script>

<style lang="scss" scoped>
	.row {
		width: 750rpx;
		height: 100vh;

		overflow-y: hidden;

		.UserInfo {
			width: 750rpx;
			height: 200rpx;
			display: block;

			.u_avatar {
				margin-top: 15rpx;
				margin-left: 20rpx;
			}

			.u_text_info {
				display: block;
				margin-left: 20rpx;
				width: 300rpx;

				.u_name {
					margin-top: 25rpx;
					font-size: 40rpx;
				}

				.u_sign {
					margin-top: 10rpx;
					font-size: 30rpx;
				}
			}

			.up_info {
				height: 30rpx;
				text-align: center;
				margin-top: 50rpx;
				margin-left: 140rpx;
				font-size: 30rpx;
				background-color: #FF5A5F;
				color: white;
				border: solid 10rpx #FF5A5F;
				border-radius: 20rpx;
			}

			.data_c {
				margin-top: 10rpx;
				display: flex;

				.data {
					font-size: 30rpx;
					margin-left: 30rpx;

					.num {
						margin-right: 10rpx;
						font-size: bold;
					}
				}
			}
		}

		.loading {
			margin-top: 50rpx;
		}

		.scroll_wrapper {
			height: calc(100vh - 200rpx - 140rpx);
			background-color: #f1f1f1;
			padding-top: 10rpx;
		}

		.ach_card {
			width: 750rpx;
			min-height: 100vh;
			height: auto;

			.ImgsBox {
				display: flex;
			}
		}
	}
</style>
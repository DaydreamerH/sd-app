<template>
	<view class="row">
		<uv-toast ref='toast'></uv-toast>
		<view class="Search">
			<uv-search v-model='con' @search="Search" @custom="Search" bgColor="white" border-color="#FF5A5F"
				color="#FF5A5F" placeholderColor="#F4A7B9" searchIconColor="#FF5A5F"></uv-search>
		</view>
		<uv-loading-icon mode="circle" color="#FF5A5F" size='30' :show='load_state'></uv-loading-icon>
		<view style="background-color:#f1f1f1;min-height: 100vh;padding-top: 10rpx;">
		<uv-empty mode="search" width="300" marginTop="100" iconColor="#F8D9E9" iconSize='130' text='暂无结果'
			textColor="#F8D9E9" textSize="20" v-if='total_pages==0&&load_state==false'></uv-empty>
		<view v-for='(imgs,index) in pairedPrevImgs' :key='index' class="ImgsBox">
			<view v-for='(img,index) in imgs' :key='img.iid'>
				<view v-if='show_time&&index==0' @click="toShow(img.iid)">
					<ImgCard v-if='show_time&&index==0' :img_url='img.source' :title='img.title'></ImgCard>
				</view>
				<view v-if='show_time&&index==1' @click="toShow(img.iid)">
					<ImgCardRight v-if='show_time&&index==1' :img_url='img.source' :title='img.title'></ImgCardRight>
				</view>
			</view>
		</view>
		<uv-load-more :status="loadAble" v-if='total_pages!=0'></uv-load-more>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				result: [],
				page: 1,
				per_page: 8,
				total_pages: '',
				show_time: false,
				con: '',
				loadAble: 'loadmore',
				iid: '',
				load_state:true
			};
		},
		methods: {
			getImg() {
				if (this.con == "") {
					this.$refs.toast.show({
						message:'请输入关键词',
						icon:'error',
						position:'top'
					})
					return false
				}
				_this.load_state = true
				let form = {}
				if (this.page == 1) {
					form = {
						page: this.page,
						per_page: this.per_page,
						con: this.con
					}
					this.show_time = false
				} else {
					form = {
						page: this.page,
						per_page: this.per_page,
						con: this.con,
						iid: this.iid
					}
				}
				let _this = this
				uni.request({
					data: form,
					method: "POST",
					url: 'http://8.137.96.56:3689/img/select_con'
				}).then(function(resp) {
					if (_this.page == 1) {
						_this.result = resp.data.img_list
						_this.show_time = true
						_this.iid = resp.data.max_iid
					} else _this.result = _this.result.concat(resp.data.img_list)
					_this.total_pages = resp.data.total_pages
					_this.load_state = false
					if (_this.total_pages == 1) _this.loadAble = 'nomore'
				})
			},
			toShow(iid) {
				uni.navigateTo({
					url: '/pages/showImg/showImg?iid=' + iid
				})
			},
			Search() {
				this.page = 1
				this.getImg()
			}
		},
		onLoad(option) {
			this.con = option.con
			const form = {
				page: this.page,
				per_page: this.per_page,
				con: this.con
			}
			let _this = this
			uni.request({
				url: 'http://8.137.96.56:3689/img/select_con',
				method: 'POST',
				data: form
			}).then(function(resp) {
				_this.result = resp.data.img_list
				_this.total_pages = resp.data.total_pages
				if (_this.total_pages == 1) _this.loadAble = 'nomore'
				_this.show_time = true
				_this.iid = resp.data.max_iid
				_this.load_state = false
			})
		},
		computed: {
			pairedPrevImgs() {
				const pairedPrevImgs = []
				for (let i = 0; i < this.result.length; i += 2) {
					const pair = this.result.slice(i, i + 2)
					pairedPrevImgs.push(pair)
				}
				return pairedPrevImgs
			}
		},
		onReachBottom() {
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
		onPullDownRefresh() {
			this.page = 1
			this.getImg()
			uni.stopPullDownRefresh()
		}
	}
</script>

<style lang="scss" scoped>
	.row {
		width: 750rpx;
		height: 100vh;

		.ImgsBox {
			display: flex;
			margin-top: 10rpx;
		}

		.Search {
			padding-top: 20rpx;
			margin-bottom: 10rpx;
			padding-left: 10rpx;
		}
	}
</style>